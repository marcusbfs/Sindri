from collections import namedtuple
from constants import R_IG
import numpy as np


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

def return_Cp(T, a0, a1, a2, a3, a4, Tmin, Tmax):
    """
    Cp/R_IG = a0 + a1*T + a2*T**2 + a3*T**3 + a4*T**4
    :param T: temperature, K
    :param a0, a1, a2, a3, a4: constants
    :return: Cp_IG, J mol-1 K-1
    """
    cp = namedtuple('Cp', ['Cp', 'msg'])
    msg = None
    if T < Tmin:
        msg = "T < Tmin"
    elif T > Tmax:
        msg = "T > Tmax"
    ans = R_IG * (a0 + a1 * T + a2 * T ** 2 + a3 * T ** 3 + a4 * T ** 4)
    ans = cp(ans, msg)
    return ans


def return_deltaH_IG(T1, T2, a0, a1, a2, a3, a4):
    ans = R_IG * (a0 * (T2 - T1) +
                  (T2 ** 2 - T1 ** 2) * a1 / 2 +
                  (T2 ** 3 - T1 ** 3) * a2 / 3 +
                  (T2 ** 4 - T1 ** 4) * a3 / 4 +
                  (T2 ** 5 - T1 ** 5) * a4 / 5
                  )
    return ans


def return_deltaS_IG(T1, T2, P1, P2, a0, a1, a2, a3, a4):
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
    if x != 0:
        return np.abs((x - y) / x)
    return np.abs(x - y)


def return_IdealGasProperties(Tref, T, Pref, P, a0, a1, a2, a3, a4, Tmin, Tmax):
    Cp_IG = return_Cp(T, a0, a1, a2, a3, a4, Tmin, Tmax)
    msg = Cp_IG.msg
    Cp_IG = Cp_IG.Cp
    dH_IG = return_deltaH_IG(Tref, T, a0, a1, a2, a3, a4)
    dS_IG = return_deltaS_IG(Tref, T, Pref, P, a0, a1, a2, a3, a4)
    dG_IG = return_deltaG_IG(dH_IG, T, dS_IG)
    dU_IG = return_deltaU_IG(dG_IG, T, dS_IG)
    dA_IG = return_deltaA_IG(dU_IG, T, dS_IG)
    dict_ans = {
        "Cp_IG": Cp_IG,
        "dH_IG": dH_IG,
        "dS_IG": dS_IG,
        "dG_IG": dG_IG,
        "dU_IG": dU_IG,
        "dA_IG": dA_IG,
        "msg": msg
    }
    return dict_ans
