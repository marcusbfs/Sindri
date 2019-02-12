import numpy as np
from constants import R_IG


def return_fluidState(P, Pc, T, Tc, Pvp, delta=1e-3):
    Pr = P / Pc
    Tr = T / Tc
    # TODO confirmar se aqui é "and" ou "or"
    if Tr > 1 and Pr > 1:
        state = "supercritical fluid"
    elif (Tr > 0.9 and Tr < 1.1) and (Pr > 0.9 and Pr < 1.1):
        state = "critical point"
    elif abs_rel_err(P, Pvp) < delta:
        state = "vapor–liquid equilibrium"
    elif P >= Pvp + delta:
        state = "compressed or unsaturated liquid"
    elif P <= Pvp - delta:
        state = "superheated steam"
    # else:
    #     state = "vapor–liquid equilibrium"

    return state


# ideal gas properties

def return_Cp(T, a0, a1, a2, a3, a4):
    """
    Cp/R_IG = a0 + a1*T + a2*T**2 + a3*T**3 + a4*T**4
    :param T: temperature, K
    :param a0, a1, a2, a3, a4: constants
    :return: Cp_IG, J mol-1 K-1
    """
    ans = R_IG * (a0 + a1 * T + a2 * T ** 2 + a3 * T ** 3 + a4 * T ** 4)

    return ans


def return_deltaH_IG(T1, T2, a0, a1, a2, a3, a4):
    # deltaH_IG = integral(T1, T2, Cp_IG, T)
    ans = R_IG * (a0 * (T2 - T1) +
                  (T2 ** 2 - T1 ** 2) * a1 / 2 +
                  (T2 ** 3 - T1 ** 3) * a2 / 3 +
                  (T2 ** 4 - T1 ** 4) * a3 / 4 +
                  (T2 ** 5 - T1 ** 5) * a4 / 5
                  )
    return ans


def return_deltaS_IG(T1, T2, P1, P2, a0, a1, a2, a3, a4):
    # deltaS_IG = integrate(T1, T2, Cp_IG/T, T) - R*ln(P2/P1)
    ans = R_IG * (
            -3 * T1 ** 4 * a4 - 4 * T1 ** 3 * a3 - 6 * T1 ** 2 * a2 - 12 * T1 * a1 +
            3 * T2 ** 4 * a4 + 4 * T2 ** 3 * a3 + 6 * T2 ** 2 * a2 + 12 * T2 * a1 - 12 * a0 * np.log(
        T1) + 12 * a0 * np.log(T2) - 12 * np.log(P2 / P1)) / 12
    return ans


def return_deltaG_IG(dH, T, dS):
    return dH - T * dS


def return_deltaU_IG(dG, T, dS):
    return dG + T * dS


def return_deltaA_IG(dU, T, dS):
    return dU - T * dS


def abs_rel_err(x, y):
    return np.abs((x - y) / x)


# residual properties

# G_R/(R*T) = integral(0, P, (Z-1)/P, dP) (constant T)


if __name__ == "__main__":
    T = 298.15
    a0 = 3.212
    a1 = 7.16e-3
    a2 = -1.528e-5
    a3 = 1.445e-8
    a4 = -.499e-11
    T1 = 298.15
    T2 = 330

    cp_IG = return_Cp(T, a0, a1, a2, a3, a4)
    deltaH_IG = return_deltaH_IG(T1, T2, a0, a1, a2, a3, a4)
    print("cp_IG: ", cp_IG)
    print("deltaH_IG: ", deltaH_IG)
