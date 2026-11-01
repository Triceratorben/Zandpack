! ---
! Copyright (C) 1996-2026 The SIESTA group
!  This file is distributed under the terms of the
!  GNU General Public License: see COPYING in the top directory
!  or http://www.gnu.org/copyleft/gpl.txt .
! ---
!> Rotation matrices for the real spherical harmonics used by Siesta
!> (spher_harm.f), in the active-rotation convention
!>   Y_lm(R rhat) = sum_{m'} D^l_{m',m}(R) Y_{lm'}(rhat)
!>
!> The rotation R is specified by the spherical angles (theta, phi) of
!> the new quantization axis z', i.e. R = Rz(phi) Ry(theta), matching
!> the zaxis/xaxis convention of m_trialorbitalclass.f90.
!>
!> Real harmonics are indexed ilm = l*l + l + m + 1 with m = -l..l.
module m_wigner_d

  use precision, only: dp

  implicit none

  private
  public :: rotation_matrix_real, is_identity_rotation, rot_matrix_3d

contains

  !> True if (theta, phi) is the identity rotation.
  logical function is_identity_rotation(theta, phi)
    real(dp), intent(in) :: theta, phi
    real(dp), parameter :: tol = 1.0e-12_dp
    is_identity_rotation = (abs(theta) < tol .and. abs(phi) < tol)
  end function is_identity_rotation

  !> 3x3 Cartesian rotation matrix for R = Rz(phi) Ry(theta).
  !> Used to rotate evaluation points/gradients in real space.
  function rot_matrix_3d(theta, phi) result(R)
    real(dp), intent(in) :: theta, phi
    real(dp)             :: R(3,3)
    real(dp) :: ct, st, cp, sp
    ct = cos(theta); st = sin(theta)
    cp = cos(phi);   sp = sin(phi)
    R(1,1) =  cp*ct;  R(1,2) = -sp;  R(1,3) =  cp*st
    R(2,1) =  sp*ct;  R(2,2) =  cp;  R(2,3) =  sp*st
    R(3,1) = -st;     R(3,2) =  0.0_dp; R(3,3) =  ct
  end function rot_matrix_3d

  !> (2l+1)x(2l+1) real rotation matrix, ordering index i = m + l + 1.
  function rotation_matrix_real(l, theta, phi) result(D)
    integer, intent(in)  :: l
    real(dp), intent(in) :: theta, phi
    real(dp)             :: D(2*l+1, 2*l+1)

    real(dp) :: d(2*l+1, 2*l+1)     ! small d-matrix d^l_{m'm}(theta)
    real(dp) :: cb, sb
    integer  :: i, j, mp, m

    cb = cos(theta / 2.0_dp)
    sb = sin(theta / 2.0_dp)
    call wigner_d_small(l, cb, sb, d)

    do i = 1, 2*l+1
      mp = i - l - 1
      do j = 1, 2*l+1
        m = j - l - 1
        D(i,j) = real_element(l, mp, m, d, phi)
      end do
    end do
  end function rotation_matrix_real

  !> Convert a small-d-matrix element into the real-basis D element,
  !> applying the azimuthal phase factors and the complex->real mixing.
  real(dp) function real_element(l, mp, m, d, phi)
    integer, intent(in)  :: l, mp, m
    real(dp), intent(in) :: d(2*l+1, 2*l+1)
    real(dp), intent(in) :: phi
    real(dp), parameter :: rs2 = 1.0_dp / sqrt(2.0_dp)
    real(dp) :: s

    s = 0.0_dp
    if (mp == 0 .and. m == 0) then
      s = d(mp+l+1, m+l+1)
    else if (mp == 0 .and. m > 0) then
      s = rs2 * ( d(mp+l+1, m+l+1) * cos(m*phi) + d(mp+l+1, -m+l+1) * sin(m*phi) )
    else if (mp == 0 .and. m < 0) then
      s = rs2 * ( d(mp+l+1, m+l+1) * cos(-m*phi) - d(mp+l+1, -m+l+1) * sin(-m*phi) )
    else if (mp > 0 .and. m == 0) then
      s = rs2 * ( d(mp+l+1, m+l+1) * cos(mp*phi) + d(-mp+l+1, m+l+1) * sin(mp*phi) )
    else if (mp < 0 .and. m == 0) then
      s = rs2 * ( d(mp+l+1, m+l+1) * cos(-mp*phi) - d(-mp+l+1, m+l+1) * sin(-mp*phi) )
    else if (mp > 0 .and. m > 0) then
      s = 0.5_dp * ( d(mp+l+1, m+l+1) * cos((mp-m)*phi) &
                   + d(mp+l+1, -m+l+1) * sin((mp+m)*phi) &
                   + d(-mp+l+1, m+l+1) * sin((mp+m)*phi) &
                   + d(-mp+l+1, -m+l+1) * cos((mp-m)*phi) )
    else if (mp > 0 .and. m < 0) then
      s = 0.5_dp * ( -d(mp+l+1, m+l+1) * sin((mp-m)*phi) &
                   + d(mp+l+1, -m+l+1) * cos((mp+m)*phi) &
                   - d(-mp+l+1, m+l+1) * cos((mp+m)*phi) &
                   + d(-mp+l+1, -m+l+1) * sin((mp-m)*phi) )
    else if (mp < 0 .and. m > 0) then
      s = 0.5_dp * ( -d(mp+l+1, m+l+1) * sin((mp-m)*phi) &
                   - d(mp+l+1, -m+l+1) * cos((mp+m)*phi) &
                   + d(-mp+l+1, m+l+1) * cos((mp+m)*phi) &
                   + d(-mp+l+1, -m+l+1) * sin((mp-m)*phi) )
    else ! mp < 0 .and. m < 0
      s = 0.5_dp * ( d(mp+l+1, m+l+1) * cos((mp-m)*phi) &
                   - d(mp+l+1, -m+l+1) * sin((mp+m)*phi) &
                   - d(-mp+l+1, m+l+1) * sin((mp+m)*phi) &
                   + d(-mp+l+1, -m+l+1) * cos((mp-m)*phi) )
    end if
    real_element = s
  end function real_element

  !> Wigner small d-matrix d^l_{m'm}(beta), rows/cols ordered m=-l..l.
  subroutine wigner_d_small(l, cb, sb, d)
    integer, intent(in)  :: l
    real(dp), intent(in) :: cb, sb
    real(dp), intent(out) :: d(2*l+1, 2*l+1)
    integer  :: i, j, mp, m
    do i = 1, 2*l+1
      mp = i - l - 1
      do j = 1, 2*l+1
        m = j - l - 1
        call wigner_d_element(l, mp, m, cb, sb, d(i,j))
      end do
    end do
  end subroutine wigner_d_small

  !> Single element d^l_{mp,m}(beta) via the explicit Wigner sum.
  subroutine wigner_d_element(l, mp, m, cb, sb, val)
    integer, intent(in)  :: l, mp, m
    real(dp), intent(in) :: cb, sb
    real(dp), intent(out) :: val
    integer  :: k, kmin, kmax
    real(dp) :: s, term, num, den
    kmin = max(0, m - mp)
    kmax = min(l + m, l - mp)
    s = 0.0_dp
    do k = kmin, kmax
      num = sqrt( fact(l+m) * fact(l-m) * fact(l+mp) * fact(l-mp) )
      den = fact(l+m-k) * fact(k) * fact(l-mp-k) * fact(k-m+mp)
      term = (-1.0_dp)**(k - m + mp) * (num / den) * &
             cb**(2*l + m - mp - 2*k) * (-sb)**(2*k - m + mp)
      s = s + term
    end do
    val = s
  end subroutine wigner_d_element

  real(dp) function fact(n)
    integer, intent(in) :: n
    integer :: i
    fact = 1.0_dp
    do i = 2, n
      fact = fact * i
    end do
  end function fact

end module m_wigner_d
