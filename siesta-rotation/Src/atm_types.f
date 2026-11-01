!
! Copyright (C) 1996-2016	The SIESTA group
!  This file is distributed under the terms of the
!  GNU General Public License: see COPYING in the top directory
!  or http://www.gnu.org/copyleft/gpl.txt.
! See Docs/Contributors.txt for a list of contributors.
!
      module atm_types

      use precision, only: dp
      use radial, only: rad_func, reset_rad_func
!
!     Derived types for orbitals,  KB projectors, and DFT+U projectors
!
      implicit none
!
!     Storage of orbital and projector real-space tables and other
!     characteristics
!
!     These parameters are over-dimensioned, but there is no storage
!     penalty, as the real information is packed and indexed.
!
      integer, parameter, public  :: maxnorbs = 100
!       Maximum number of nlm orbitals
!
      integer, parameter, public  :: maxn_pjnl = 40
!       Maximum number of projectors (not counting different "m" copies)
      integer, parameter, public  :: maxn_orbnl = 200
!       Maximum number of nl orbitals (not counting different "m" copies)
!       Now very large to accommodate filteret basis sets
      integer, parameter, public  :: maxnprojs = 200
!       Maximum number of nlm projectors
!

!
!     Species_info: Consolidate all the pieces of information in one place
!
      type, public :: species_info
         character(len=2)                ::  symbol
         character(len=20)               ::  label
         integer                         ::  z          ! Atomic number
         real(dp)                        ::  mass
         real(dp)                        ::  zval       ! Valence charge
         real(dp)                        ::  self_energy !Electrostatic
                                                         !self-energy
!
!        Orbitals
!             We keep track of just one orbital for each
!             "nl" family
!
         integer                         ::  n_orbnl=0  ! num of nl orbs
         integer                         ::  lmax_basis=0 ! basis l cutoff
         integer, dimension(maxn_orbnl)  ::  orbnl_l    ! l of each nl orb
         integer, dimension(maxn_orbnl)  ::  orbnl_n    ! n of each nl orb
         integer, dimension(maxn_orbnl)  ::  orbnl_z    ! z of each nl orb
         logical, dimension(maxn_orbnl)  ::  orbnl_ispol! is it a pol. orb?

         real(dp),
     $            dimension(maxn_orbnl)  ::  orbnl_pop  ! pop. of nl orb
                                                        ! (total of 2l+1
                                                        ! components)
!
!        KB Projectors
!             For each l, there can be several projectors. Formally, we
!             can can use the "nl" terminology for them. n will run from
!             1 to the total number of projectors at that l.
!
!
         logical                         ::  lj_projs = .false.
         integer                         ::  n_pjnl=0   ! num of "nl" projs
         integer                         ::  lmax_projs=0 ! l cutoff for projs
         integer, dimension(maxn_pjnl)   ::  pjnl_l     ! l of each nl proj
         real(dp), dimension(maxn_pjnl)  ::  pjnl_j     ! j of each nl proj
         integer, dimension(maxn_pjnl)   ::  pjnl_n     ! n of each nl proj
         real(dp), dimension(maxn_pjnl)
     $                                   ::  pjnl_ekb   ! energy of
                                                        ! each nl proj

!
!        Aggregate numbers of orbitals and projectors (including 2l+1
!        copies for each "nl"), and index arrays keeping track of
!        which "nl" family they belong to, and their n, l, and m (to avoid
!        a further dereference)
!
         integer                         ::  norbs=0
         integer, dimension(maxnorbs)    ::  orb_index
         integer, dimension(maxnorbs)    ::  orb_n
         integer, dimension(maxnorbs)    ::  orb_l
         integer, dimension(maxnorbs)    ::  orb_m
         integer, dimension(maxnorbs)    ::  orb_gindex
         real(dp),
     $            dimension(maxnorbs)    ::  orb_pop   ! pop. of nl orb
!
!        Optional per-orbital rotation (polar theta, azimuthal phi)
!        in radians. Default (0,0) = identity. Applied via Wigner-D
!        mixing of the m components in the spherical-harmonic tables.
!
         real(dp), dimension(maxnorbs)   ::  orb_rot_theta = 0.0_dp
         real(dp), dimension(maxnorbs)   ::  orb_rot_phi   = 0.0_dp

         integer                         ::  nprojs=0
         integer, dimension(maxnprojs)   ::  pj_index
         integer, dimension(maxnprojs)   ::  pj_n
         integer, dimension(maxnprojs)   ::  pj_l
         real(dp), dimension(maxnprojs)  ::  pj_j
         integer, dimension(maxnprojs)   ::  pj_m
         integer, dimension(maxnprojs)   ::  pj_gindex
!        DFT+U Projectors
!        Here we follow the scheme used for the KB projectors
!
         integer                         ::  n_pjdftunl = 0
                                             ! num of "nl" projs
                                             ! not counting the "m copies"
         integer                         ::  lmax_dftu_projs = 0
                                             ! l cutoff for DFT+U proj
         integer, dimension(maxn_pjnl)   ::  pjdftunl_l ! l of each nl proj
         integer, dimension(maxn_pjnl)   ::  pjdftunl_n ! n of each nl proj
                                             ! Here, n is not the principal
                                             ! quantum number, but a sequential
                                             ! index from 1 to the total
                                             ! number of projectors for that l.
                                             ! In the case of DFT+U projectors,
                                             ! It is always equal to 1.
         real(dp), dimension(maxn_pjnl)  ::  pjdftunl_U ! U of each nl projector
         real(dp), dimension(maxn_pjnl)  ::  pjdftunl_J ! J of each nl projector

         integer                         ::  nprojsdftu = 0
                                             ! Total number of DFT+U proj.
                                             ! counting the "m copies"
                                             ! (including the (2l + 1) factor))
         integer, dimension(maxnprojs)   ::  pjdftu_index = 0
         integer, dimension(maxnprojs)   ::  pjdftu_n = 0
         integer, dimension(maxnprojs)   ::  pjdftu_l = 0
         integer, dimension(maxnprojs)   ::  pjdftu_m = 0
         integer, dimension(maxnprojs)   ::  pjdftu_gindex = 0
         type(dftu_so_integrals_type), dimension(:), pointer
     .                                   ::  dftu_so_integrals => null()
!
         type(rad_func), dimension(:), pointer       ::  orbnl => null()
         type(rad_func), dimension(:), pointer       ::  pjnl => null()
         type(rad_func), dimension(:), pointer       ::  pjdftu =>null()
         type(rad_func)                              ::  vna
         integer                                     ::  vna_gindex=0
         type(rad_func)                              ::  chlocal
         type(rad_func)                              ::  reduced_vlocal
         logical                                     ::  there_is_core
         type(rad_func)                              ::  core

         logical                        :: read_from_file
      contains
         procedure :: reset => reset_species_info
      end type species_info

!     Derived type for the definition of the on-site four-center-integrals
!     required for LDA+U + Spin orbit
      type, public ::  dftu_so_integrals_type
         real(dp), dimension(:), pointer :: Slater_F
                                             ! Slater integrals,
                                             !   involving the radial part
                                             !   of the atomic wave funcs.
                                             !   Used when LDA+U is used
                                             !   together with Spin-Orbit
                                             !   or non-collinear
                                             !   magnetism
         real(dp), dimension(:,:,:,:), pointer :: vee_4center_integrals
                                             ! Values of the four center
                                             !   integrals with the
                                             !   electron–electron
                                             !   interactions, that are
                                             !   expressed as the
                                             !   integrals of the Coulomb
                                             !   kernel on the
                                             !   wave functions of the
                                             !   localized basis set
                                             !   (e.g. d atomic states)
                                             !   Used when LDA+U is used
                                             !   together with Spin-Orbit
                                             !   or non-collinear
                                             !   magnetism
      contains
         procedure :: reset => reset_dftu_so_integrals
      end type dftu_so_integrals_type



!
      integer, save, public             :: nspecies
      integer, save, public             :: npairs

      type(species_info), target, allocatable,
     $                            save, public   ::  species(:)
      type(rad_func), allocatable, target,
     $                            save, public   ::  elec_corr(:)


      public :: atm_types_reset
      private

      contains

      subroutine reset_species_info( self )
            !! Deallocates all associated pointers within a given species.
            implicit none
            class(species_info), intent(inout) :: self
            integer :: idftu

            if ( associated(self%dftu_so_integrals) ) then
               do idftu = 1, size( self%dftu_so_integrals, 1 )
                  call self%dftu_so_integrals(idftu)%reset()
               enddo
               deallocate( self%dftu_so_integrals )
               nullify( self%dftu_so_integrals )
            endif

            if ( associated(self%orbnl) ) then
               do idftu = 1, size( self%orbnl, 1 )
                  call reset_rad_func( self%orbnl(idftu))
               enddo
               deallocate( self%orbnl )
            endif
            if ( associated(self%pjnl) ) then
               do idftu = 1, size( self%pjnl, 1 )
                  call reset_rad_func( self%pjnl(idftu))
               enddo
               deallocate( self%pjnl )
            endif
            if ( associated(self%pjdftu) ) then
               do idftu = 1, size( self%pjdftu, 1 )
                  call reset_rad_func( self%pjdftu(idftu))
               enddo
               deallocate( self%pjdftu )
            endif

            nullify( self%pjnl, self%orbnl, self%pjdftu )

            call reset_rad_func( self%vna )
            call reset_rad_func( self%chlocal )
            call reset_rad_func( self%reduced_vlocal )
            call reset_rad_func( self%core )
      end subroutine reset_species_info

      subroutine reset_dftu_so_integrals( self )
            !! Deallocates all associated pointers for DFTU-SO integrals.
            implicit none
            class(dftu_so_integrals_type), intent(inout) :: self

            if ( associated(self%Slater_F) )
     &         deallocate( self%Slater_F )
            if ( associated(self%vee_4center_integrals) )
     &         deallocate( self%vee_4center_integrals )

            nullify( self%Slater_F, self%vee_4center_integrals )

      end subroutine reset_dftu_so_integrals

      subroutine atm_types_reset()
            implicit none
            integer :: ispec
            if ( allocated(species) ) then
                  do ispec = 1, size(species,1)
                        call species(ispec)%reset()
                  enddo
                  deallocate( species )
            endif

            if ( allocated(elec_corr) ) then
                  do ispec = 1, size(elec_corr,1)
                        call reset_rad_func( elec_corr(ispec) )
                  enddo
                  deallocate(elec_corr)
            endif
      end subroutine atm_types_reset

      end module atm_types
