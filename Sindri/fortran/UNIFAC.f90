subroutine getGamma(x, T, n, m, amk, vk, Rk, Qk, gamma1)
    implicit none

    integer, intent(in) :: n, m
    real(8), dimension(n), intent(in) :: x
    real(8), dimension(m), intent(in) :: Rk, Qk
    integer, dimension(n,m), intent(in) :: vk
    real(8), dimension(m,m), intent(in) ::amk
    real(8), intent(in) :: T
    real(8), dimension(n), intent(out) :: gamma1
    integer :: ii, kk
    real(8) :: sum_rx, sum_qx

    real(8) :: r(n), q(n), e(m,n), beta(n,m), theta(m), s(m),L(n),J(n),ln_gamma_C(n), ln_gamma_R(n), tau(m,m)

    tau = exp(-amk/T) 

    do ii=1,n
        r(ii) = sum(vk(ii,:)*Rk(:))
        q(ii) = sum(vk(ii,:)*Qk(:))
    enddo

    sum_rx = sum(x*r)
    sum_qx = sum(x*q)

    ! r, q
    do ii=1,n 
        e(:, ii) = vk(ii,:)*Qk(:)/q(ii)
    enddo

    ! beta
    do ii=1, n
        do kk=1, m
            beta(ii,kk) = sum(e(:,ii)*tau(:,kk))
        end do
    end do

    do kk=1,m
        theta(kk) = sum(x*q*e(kk,:))
    end do
    theta = theta/sum_qx

    do kk=1,m
        s(kk) = sum(theta*tau(:,kk))
    end do

    J = r/sum_rx
    L = q/sum_qx
    ln_gamma_C = 1.0_8 - J + log(J) - 5.0_8*q*(1.-J/L+log(J/L))

    do ii=1,n
        ln_gamma_R(ii) = q(ii)*(1.0_8 - sum(theta*beta(ii,:)/s - e(:,ii)*log(beta(ii,:)/s)))
    end do

    gamma1 = exp(ln_gamma_C + ln_gamma_R)

end subroutine

subroutine getGammaTrange(x, T, l, n, m, amk, vk, Rk, Qk, gammas)
    implicit none
    integer, intent(in) :: n, m,l
    real(8), dimension(n), intent(in) :: x
    real(8), dimension(m), intent(in) :: Rk, Qk
    integer, dimension(n,m), intent(in) :: vk
    real(8), dimension(m,m), intent(in) ::amk
    real(8), intent(in) :: T(l)
    real(8), dimension(l,n), intent(out) :: gammas
    integer :: ii
    do ii=1, l
        call getGamma(x,T(ii),n,m,amk,vk,Rk,Qk, gammas(ii,:))
    end do
end subroutine