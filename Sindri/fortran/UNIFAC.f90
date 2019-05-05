subroutine getGamma(x, T, n, m, amk, vk, Rk, Qk, gamma1)
    implicit none

    integer, intent(in) :: n, m
    real(8), dimension(n), intent(in) :: x
    real(8), dimension(m), intent(in) :: Rk, Qk
    integer, dimension(n,m), intent(in) :: vk
    real(8), dimension(m,m), intent(in) ::amk
    real(8), intent(in) :: T
    real(8), dimension(n), intent(out) :: gamma1
    integer :: ii,jj,kk
    real(8) :: s1, s2, sum_rx, sum_qx

    !real(8), intent(in) :: x(n), T, vk(n,m), amk(m,m), Rk(m), Qk(m)
    real(8) :: r(n), q(n), e(m,n), beta(n,m), theta(m), s(m),L(n),J(n),ln_gamma_C(n), ln_gamma_R(n), tau(m,m)

    do ii=1, m
        do jj=1, m
            tau(ii,jj) = exp(-amk(ii,jj)/T)
        end do
    end do

    do ii=1,n
        s1 = 0.0_8
        s2 = 0.0_8
        do jj=1,m
            s1 = s1 + vk(ii,jj)*Rk(jj)
            s2 = s2 + vk(ii,jj)*Qk(jj)
        end do
        r(ii) = s1
        q(ii) = s2
    enddo

    sum_rx = 0.0_8
    sum_qx = 0.0_8

    do ii=1,n
        sum_rx = sum_rx + x(ii)*r(ii)
        sum_qx = sum_qx + x(ii)*q(ii)
    end do

    ! r,q
    do kk=1, m
        do ii=1, n
            e(kk,ii) = vk(ii,kk)*Qk(kk)/q(ii)
        end do
    end do

    ! beta
    beta = 0.0_8
    do ii=1, n
        do kk=1, m
             do jj=1, m
                beta(ii,kk) = beta(ii,kk) + e(jj,ii) * tau(jj,kk)
            end do
        end do
    end do

    do kk=1,m
        s1 = 0.0_8
        do ii=1, n
            s1 = s1 + x(ii)*q(ii)*e(kk,ii)
        end do
        theta(kk) = s1/sum_qx
    end do

    s = 0.0_8
    do kk=1,m
        do jj=1,m
            s(kk) = s(kk) + theta(jj)*tau(jj,kk)
        end do
    end do

    do ii=1,n
        J(ii) = r(ii)/sum_rx
        L(ii) = q(ii)/sum_qx
        ln_gamma_C(ii) = 1.0_8 - J(ii) + log(J(ii)) - 5.0_8*q(ii)*(1.-J(ii)/L(ii)+log(J(ii)/L(ii)))
        s1 = 0.0_8
        do kk=1,m
            s1 = s1 + theta(kk)*beta(ii,kk)/s(kk) - e(kk,ii)*log(beta(ii,kk)/s(kk))
        end do
        ln_gamma_R(ii) = q(ii)*(1.0_8 - s1)

        gamma1(ii) = exp(ln_gamma_C(ii) + ln_gamma_R(ii))
    end do

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
