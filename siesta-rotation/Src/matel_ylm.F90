!
! Copyright (C) 1996-2016 The SIESTA group
! This file is distributed under the terms of the
! GNU General Public License: see COPYING in the top directory
! or http://www.gnu.org/copyleft/gpl.txt.
! See Docs/Contributors.txt for a list of contributors.
!
!
!> This module implements a data structure and associated procedures to
!> handle the expansion in spherical harmonics of the functions in the
!> 'matel registry', and their fourier transforms, as a first step in
!> the computation of two-center integrals (See Siesta paper). In this
!> context, several "functions" might be associated to the same object
!> in the registry: for example, a given PAO with index 'ig' might be
!> just 'evaluate'd, or 'x_evaluate'd (multiplied by x), etc. Note that
!> *most* of the functions we deal with are "pure" (PAOs, KBs, and LDAU
!> projectors are of the form f(r)Y_lm(theta,phi) already, so most of
!> the dereferencing done here is superfluous. We have, on the other
!> hand, {x,y,z}*{PAO,KB} (which involve Y_(l+1),m)
!> and the wannier projectors, which might not be "pure". 
!> More complex matrix elements might conceivably be implemented.      

!> The computations are done in parallel and the results replicated
!> ("all-reduced") in in all processors.
      
!> Initial implementation: Rogeli Grima (BSC)
!> Clarifications and some enhancements: Alberto Garcia (ICMAB)
module matel_ylm_m

  use matel_params_m, only: NQ, RMAX
  
  use precision, only : dp
  use alloc,     only : re_alloc, de_alloc, alloc_default, &
                        allocDefaults
  use sys,       only: die
  use parallel,  only : Node, Nodes
  use m_radfft,  only : radfft, reset_radfft

  use m_matel_registry, only: LCUT
  
  use spher_harm, only : RLYLM, YLMEXP, lofilm
  use m_wigner_d, only: rotation_matrix_real, is_identity_rotation
  private

  integer, save :: num_orb_max = 0  ! cached count of pure PAOs (set serially)

  ! Parameters
  real(dp),         parameter :: EXPAND    =  1.20_dp
  integer,          parameter :: MINEXPAND =  32
  character(len=*), parameter :: MYNAME    =  'MATEL_YLM'

  !> This really holds the expansion of a set of functions in spherical-harmonics 
  !> Indexing arrays could be avoided if we kept the information of a given function
  !> in a simpler derived type instead, and making this an _array_ of the simpler elements.
  type, public :: SPHER_HARM_t
    integer           :: N           ! Number of orbitals/projectors
    integer           :: BASE        ! Base for registry index count
    real(dp), pointer :: F(:,:)      => null() ! Radial expansion for each spherical harmonic
    integer,  pointer :: ILM(:)      => null() ! Spherical harmonics indexes (packed l,m)
    integer,  pointer :: IND(:)      => null() ! Number of spherical harmonics (after COMPUTE_SPHA)
                                              ! Index of harmonics (after REDUCE_SPHA)
    integer,  pointer :: INVP(:)     => null() ! Map from harmonic components to the associated function

    contains
      procedure :: COMPUTE_SPHA
      procedure :: GET_DIM
      procedure :: HARM2ORB
      procedure :: INDF
      procedure :: DELETE
      ! now called internally by 'compute_spha'
      procedure, private :: REDUCE_SPHA
  end type SPHER_HARM_t

contains

  subroutine COMPUTE_SPHA(this, first_gindex, last_gindex, func, l_inc)
    !     Find the spherical-harmonic decomposition of a set of functions
    !     from the 'matel-registry'      
    !     The operations are performed in parallel

    implicit none
    
    class(SPHER_HARM_t) :: this

    !> First and last global registry indexes of the set of functions
    integer, intent(in) :: first_gindex, last_gindex

    !> Function to be decomposed. Typically it is "evaluate", as in
    !> the 'matel-registry' interface. It can include an implicit
    !> matrix element function (for example, 'evaluate_x' includes the
    !> product by 'x' of radial functions).

    !> The evaluator selects the function on the basis of a single index 'ig'
    !> that is de-referenced in the 'matel_registry'. It returns the value and the gradient.
    interface
      subroutine func(ig, rvec, yy, grady)
        use precision, only : dp
        integer, intent(in)   :: ig
        real(dp), intent(in)  :: rvec(3)
        real(dp), intent(out) :: yy, grady(3)
      end subroutine func
    end interface

    !> When the implied matrix element function increases the maximum l
    !> e.g. for x*\Phi, the maximum l is increased by 1, so l_inc=1
    integer, intent(in) :: l_inc

    ! Local variables
    integer :: i, ig, il, first, last, nlocal, nf, mf, l, nilm, jlm

    this%N      = last_gindex - first_gindex + 1
    this%BASE   = first_gindex - 1  ! this is the base for counting

    ! Split the work on the N functions among processors
    nlocal      = GET_LOOP_LIMITS(this%N, Node, first, last)
    nf          = 0

    ! Allocate space
    nullify(this%IND,this%F,this%ILM,this%INVP)
    call RE_ALLOC(this%IND, 1, this%n+1, 'F', MYNAME)
    mf = MAX(INT(nlocal*EXPAND), nlocal+MINEXPAND)
    call RE_ALLOC(this%INVP, 1, MF, 'INVP', MYNAME)
    call RE_ALLOC(this%F, 0, NQ, 1, MF, 'F', MYNAME)
    call RE_ALLOC(this%ILM, 1, MF, 'ILM', MYNAME)

    ! Iterate local orbitals
    do IL = first, last
      ! Get the Global Index of the orbital
      IG = this%BASE+IL
      l = LCUT(IG)            ! Maximum l
      nilm = (l+2)**2         ! Total maximum number of l,m indexes
      ! Check if we have enough memory
      if (nf+nilm > mf) then
        mf = (nf+NILM)*EXPAND
        call RE_ALLOC(this%INVP, 1, mf, 'INVP', MYNAME)
        call RE_ALLOC(this%F, 0, NQ, 1, mf, 'F', MYNAME)
        call RE_ALLOC(this%ILM, 1, mf, 'ILM', MYNAME)
      endif
      ! Compute Spherical harmonic expansion of orbital IG
      call YLMEXP(L+L_INC, RLYLM, func, IG, 0, NQ, RMAX, NILM, &
                this%ILM(nf+1:), this%F(:,nf+1:))
      ! Apply optional per-orbital rotation (Wigner-D mixing of m comps)
      if (IG .le. num_orb_max) then
        call apply_orbital_rotation(IG, L, NILM, this%ILM(nf+1:), &
                this%F(:,nf+1:))
      endif
      ! Store orbital in Fourier space
      do JLM = 1, NILM
        nf = nf + 1
        ! Save the orbital ID of current harmonic
        this%INVP(nf) = IL
        l = LOFILM(this%ILM(nf))
        call RADFFT(L, NQ, RMAX, this%F(0:NQ,NF), this%F(0:NQ,NF))
        ! F(NQ,NF) = 0._dp
      enddo
      this%IND(IL) = NILM
    enddo

    ! Replicate data to all processors
    call REDUCE_SPHA(this)

  end subroutine COMPUTE_SPHA

  !> Mix the m-components of a pure (l,m) orbital's spherical-harmonic
  !> expansion with the Wigner-D rotation matrix for the orbital's
  !> (theta, phi). Serial/single-rank path: IG is the global orbital
  !> index (1..num_orb for PAOs). No-op for identity rotations.
  subroutine apply_orbital_rotation(IG, L, NILM, ILM_loc, F_loc)
    use atm_types, only: nspecies, species
    integer, intent(in)    :: IG, L, NILM
    integer, intent(inout) :: ILM_loc(NILM)
    real(dp), intent(inout):: F_loc(0:NQ, NILM)

    integer :: is, io, l, m, ilm, i, j, mp, ioff
    real(dp) :: theta, phi
    real(dp), allocatable :: D(:,:), Ftmp(:,:)

    ! Locate (is, io) for this global PAO index
    call gindex_to_orb(IG, is, io)
    if (is <= 0) return
    l = species(is)%orb_l(io)
    if (l == 0) return
    theta = species(is)%orb_rot_theta(io)
    phi   = species(is)%orb_rot_phi(io)
    if (is_identity_rotation(theta, phi)) return

    allocate(D(2*l+1, 2*l+1), Ftmp(0:NQ, 2*l+1))
    D = rotation_matrix_real(l, theta, phi)

    ! Collect the (2l+1) m-components of this orbital into Ftmp
    Ftmp = 0.0_dp
    do j = 1, NILM
      ilm = ILM_loc(j)
      m = ilm - l*l - l - 1
      if (abs(m) <= l) Ftmp(:, m+l+1) = F_loc(:, j)
    end do
    ! Rotate: F'_{m'} = sum_m D(m',m) F_m
    do i = 1, 2*l+1
      mp = i - l - 1
      F_loc(:, :) = 0.0_dp
      do j = 1, NILM
        ilm = ILM_loc(j)
        m = ilm - l*l - l - 1
        if (abs(m) <= l) F_loc(:, j) = F_loc(:, j) + D(i, m+l+1) * Ftmp(:, m+l+1)
      end do
    end do
    deallocate(D, Ftmp)
  end subroutine apply_orbital_rotation

  !> Map a global PAO index (1..num_orb) to (species, per-species io).
  subroutine gindex_to_orb(IG, is, io)
    use atm_types, only: nspecies, species
    integer, intent(in)  :: IG
    integer, intent(out) :: is, io
    integer :: acc, k
    acc = 0
    is = 0
    do k = 1, nspecies
      if (IG .gt. acc .and. IG .le. acc + species(k)%norbs) then
        is = k
        io = IG - acc
        return
      endif
      acc = acc + species(k)%norbs
    end do
    io = 0
  end subroutine gindex_to_orb

  subroutine REDUCE_SPHA(this)
    ! Reduce the Spherical Harmonics
    ! Reduce the values of the different arrays of SPHER_HARM_t.
    ! At input, IND contains the number of harmonics of every orbital.
    ! At exit, it can be used to index the harmonics of every orbital
    
#ifdef MPI
    use m_matel_registry, only : is_inter_node
    use m_matel_registry, only : INTRA_NODE_COMM, INTER_NODE_COMM
    use mpi_siesta, only : MPI_INTEGER, MPI_COMM_WORLD, MPI_Allgatherv
    use mpi_siesta, only : MPI_DOUBLE_PRECISION, MPI_IN_PLACE
    use mpi_siesta, only : MPI_Gatherv, MPI_Bcast
#endif
    implicit none

    class(SPHER_HARM_t) :: this

    ! Local variables
    integer           :: i, ig, first, last, nf, prev
#ifdef MPI
    integer           :: MPIERR
    integer,  pointer :: COUN1(:) => null(), DISP1(:) => null()
    integer,  pointer :: COUN2(:) => null(), DISP2(:) => null()
    real(dp), pointer :: G_F(:,:) => null()
    integer,  pointer :: G_ILM(:) => null(), G_INVP(:) => null()
#endif
    external :: timer
    call timer( 'gatherv_SPHA', 1 )

#ifdef MPI
    ! reduce IND array in place
    if (NODES > 1) then
      nullify(COUN1,DISP1)
      call RE_ALLOC(COUN1, 0, NODES-1, 'COUN1,', MYNAME)
      call RE_ALLOC(DISP1, 0, NODES, 'DISP1,', MYNAME)
      DISP1(0) = 0
      do I = 0, NODES-1
        COUN1(I) = GET_LOOP_LIMITS(this%n, I, first, last)
        DISP1(I+1) = DISP1(I) + COUN1(I)
      enddo
      call MPI_Allgatherv(MPI_IN_PLACE, COUN1(NODE), MPI_INTEGER, &
        this%IND, COUN1, DISP1, MPI_INTEGER, MPI_COMM_WORLD, MPIERR)
    endif
#endif

    ! IND array should be acumulative
    prev = this%IND(1)
    this%IND(1) = 1
    do I = 1, this%N
      IG = prev + this%IND(I)
      prev = this%IND(I+1)
      this%IND(I+1) = IG
    enddo

#ifdef MPI
    if (NODES > 1) then
      ! Reduce INVP, ILM and F between processors
      nullify(coun2,disp2)
      call RE_ALLOC(COUN2, 0, NODES-1, 'COUN2,', MYNAME)
      call RE_ALLOC(DISP2, 0, NODES, 'DISP2,', MYNAME)
      DISP2(0) = 0
      nf = 0
      do I = 0, NODES-1
        DISP2(I+1) = this%IND(DISP1(I+1)+1)-1
        COUN2(I) = DISP2(I+1) - DISP2(I)
      enddo
      nf = DISP2(NODES)

      ! Allocate arrays and reduce INVP
      nullify(G_INVP)
      call RE_ALLOC(G_INVP, 1, nf, 'INVP', MYNAME)

!      call MPI_Allgatherv(this%INVP, COUN2(NODE), MPI_INTEGER, &
!        G_INVP, COUN2, DISP2, MPI_INTEGER, MPI_COMM_WORLD, MPIERR)
      call MPI_Gatherv(this%INVP, COUN2(NODE), MPI_INTEGER, &
        G_INVP, COUN2, DISP2, MPI_INTEGER, 0, MPI_COMM_WORLD, MPIERR)
      if (is_inter_node) call MPI_Bcast( G_INVP, DISP2(NODES), MPI_INTEGER, &
                                         0, INTER_NODE_COMM, MPIERR)
      call MPI_Bcast( G_INVP, DISP2(NODES), MPI_INTEGER, &
                      0, INTRA_NODE_COMM, MPIERR)

      call DE_ALLOC(this%INVP, 'INVP', MYNAME)
      this%INVP => G_INVP

      ! Allocate arrays and reduce ILM
      nullify(G_ILM)
      call RE_ALLOC(G_ILM, 1, nf, 'ILM', MYNAME)

!      call MPI_Allgatherv(this%ILM, COUN2(NODE), MPI_INTEGER, &
!        G_ILM, COUN2, DISP2, MPI_INTEGER, MPI_COMM_WORLD, MPIERR)
      call MPI_Gatherv(this%ILM, COUN2(NODE), MPI_INTEGER, &
        G_ILM, COUN2, DISP2, MPI_INTEGER, 0, MPI_COMM_WORLD, MPIERR)
      if (is_inter_node) call MPI_Bcast( G_ILM, DISP2(NODES), MPI_INTEGER, &
                                         0, INTER_NODE_COMM, MPIERR)
      call MPI_Bcast( G_ILM, DISP2(NODES), MPI_INTEGER, &
                      0, INTRA_NODE_COMM, MPIERR)

      call DE_ALLOC(this%ILM, 'ILM', MYNAME)
      this%ILM => G_ILM

      ! Allocate arrays and reduce F
      COUN2 = COUN2*(NQ+1)
      DISP2 = DISP2*(NQ+1)
      nullify(G_F)
      call RE_ALLOC(G_F, 0, NQ, 1, nf, 'F', MYNAME)

!      call MPI_Allgatherv(this%F, COUN2(NODE), &
!        MPI_DOUBLE_PRECISION, G_F, COUN2, DISP2, &
!        MPI_DOUBLE_PRECISION, MPI_COMM_WORLD, MPIERR)
      call MPI_Gatherv(this%F, COUN2(NODE), &
        MPI_DOUBLE_PRECISION, G_F, COUN2, DISP2, &
        MPI_DOUBLE_PRECISION, 0, MPI_COMM_WORLD, MPIERR )
      if (is_inter_node) call MPI_Bcast( G_F, DISP2(NODES), MPI_DOUBLE_PRECISION, &
                                         0, INTER_NODE_COMM, MPIERR)
      call MPI_Bcast( G_F, DISP2(NODES), MPI_DOUBLE_PRECISION, &
                      0, INTRA_NODE_COMM, MPIERR)

      call DE_ALLOC(this%F, 'F', MYNAME)
      this%F => G_F

      ! Dealloc temporal arrays
      call DE_ALLOC(COUN2, 'COUN2,', MYNAME)
      call DE_ALLOC(DISP2, 'DISP2,', MYNAME)
      call DE_ALLOC(COUN1, 'COUN1,', MYNAME)
      call DE_ALLOC(DISP1, 'DISP1,', MYNAME)
    endif
#endif
    call timer( 'gatherv_SPHA', 2 )
  end subroutine REDUCE_SPHA

  function GET_DIM(this, n) result(d)
    ! Returns the accumulated number of spherical-harmonic terms at position n
    ! of the 'Spha' data structure, as tracked by the pointer array IND.
    ! The total number of terms is get_dim(this%N)
    ! INPUT:
    !   integer n : position to check. (1 <= n <= this%N)
    ! OUTPUT:
    !   integer d : Number of terms
    
    implicit none
    class(SPHER_HARM_t) :: this
    integer, intent(in) :: n
    integer             :: d
    
    d = this%IND(n+1)-1
  end function GET_DIM

  function Harm2Orb(this, id) result(d)
    ! Returns the global registry Id of the function from which the current harmonic
    ! originates.
    ! INPUT:
    !   integer id : harmonic Id
    ! OUTPUT:
    !   integer d  : Orbital Id
    
    implicit none
    class(SPHER_HARM_t) :: this
    integer, intent(in) :: id
    integer             :: d
    
    d = this%Invp(id)
  end function Harm2Orb

  function INDF(this, id) result(d)
    ! Return the index of the first harmonic of an orbital
    ! INPUT:
    !   integer id : Orbital Id
    ! OUTPUT:
    !   integer d  : Harmonic Id
    
    implicit none
    class(SPHER_HARM_t) :: this
    integer, intent(in) :: id
    integer             :: d
    
    d = this%Ind(id-this%BASE)
  end function INDF

  function GET_LOOP_LIMITS(N, ID, FIRST, LAST) RESULT(SIZE)
    ! Get the loop limits resulting to split N elements between Nodes
    ! INPUT:
    !   integer N  : Number of elements to distribute
    !   integer ID : Id of the Node
    ! OUTPUT:
    !   integer FIRST : first element of the loop
    !   integer LAST  : last element of the loop
    !   integer SIZE  : Number of elements of the loop
    
    implicit none
    integer, intent(in)  :: N, ID
    integer, intent(out) :: FIRST, LAST
    integer              :: size, di, mo
    
    if (NODES == 1) then
      FIRST = 1
      LAST  = N
    else
      di    = N / NODES
      mo    = MOD(N, NODES)
      FIRST = 1 + ID*di + MIN(ID, mo)
      LAST  = (ID+1)*di + MIN(ID+1, mo)
    endif
    SIZE = LAST - FIRST + 1
  end function GET_LOOP_LIMITS

  subroutine DELETE(this)
    ! Deallocates all arrays in the SPHER_HARM_t type and resets scalars
    
    implicit none
    class(SPHER_HARM_t) :: this
    
    ! Local variables
    character(len=*), parameter :: MYNAME = 'SPHER_HARM_DELETE'

    ! Deallocate all pointer arrays
    if (associated(this%F)) then
      call de_alloc(this%F, 'F', MYNAME)
    endif
    nullify(this%F)

    if (associated(this%ILM)) then
      call de_alloc(this%ILM, 'ILM', MYNAME)
    endif
    nullify(this%ILM)

    if (associated(this%IND)) then
      call de_alloc(this%IND, 'IND', MYNAME)
    endif
    nullify(this%IND)

    if (associated(this%INVP)) then
      call de_alloc(this%INVP, 'INVP', MYNAME)
    endif
    nullify(this%INVP)

    ! Reset scalars
    this%N = 0
    this%BASE = 0

  end subroutine DELETE

end module matel_ylm_m
