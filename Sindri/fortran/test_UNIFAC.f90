program test_UNIFAC
implicit none

integer, parameter  :: n =2, m=3
real(8) :: t
real(8) :: x(n) = (/ .4_8 ,.6_8 /)
real(8) :: qk(m) = (/ .848_8, .54_8, .936_8 /)
real(8) :: rk(m) = (/.9011_8,  .6744_8, 1.207_8 /)
real(8) :: amk(m,m), gamma1(n), expected_gamma(n) = (/ 1.133_8, 1.047_8/)
integer :: vk(n,m)
logical :: equal

t = 308.15_8

vk(1,1) = 2
vk(1,2) = 1
vk(1,3) = 1

vk(2,1) = 2
vk(2,2) = 5
vk(2,3) = 0

amk(1,1) = 0.0_8
amk(1,2) = 0.0_8
amk(1,3) = 255.7

amk(2,1) = 0.0_8
amk(2,2) = 0.0_8
amk(2,3) = 255.7

amk(3,1) = 65.33_8
amk(3,2) = 65.33_8
amk(3,3) = 0.0_8

call getGamma(x, t, n, m, amk, vk, rk, qk, gamma1)
call is_equal_arr(gamma1, expected_gamma, n, equal)

write(*,*) expected_gamma
write(*,*) gamma1
if (.not. equal) then
    write(*,*) "Test failed"
else
    write(*,*) "Test passed"
endif


end program test_UNIFAC

subroutine is_equal_arr(a, b, n, ans)
    integer, intent(in) :: n
    real(8), intent(in) ::a(n), b(n)
    logical, intent(out) :: ans
    integer :: i
    real(8) :: tol = 1e-4
    ans = .true.
    
    do i=1, n
        if (abs(a(i)- b(i)) .ge. tol ) then
            ans = .false.
            return
        end if
    enddo
end subroutine