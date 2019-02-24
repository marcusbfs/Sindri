from collections import namedtuple
import numpy as np
from constants import R_IG

# from numba import jit

state_dict = {
    # It must have the following order:
    #   supercritical, critical point, vapor-liquid equi., liquid, vapor.
    "supercritical": "supercritical fluid",
    "critical_point": "critical point",
    "VL_equi": "vapor-liquid equilibrium",
    "liq": "compressed or unsaturated liquid",
    "vap": "superheated steam",
}

state_options = list(state_dict.values())


def return_fluidState(P, Pc, T, Tc, Pvp, delta=1e-3):
    Pr = P / Pc
    Tr = T / Tc
    if Tr > 1 or Pr > 1:
        state = state_dict["supercritical"]
    elif (Tr > 0.9 and Tr < 1.1) and (Pr > 0.9 and Pr < 1.1):
        state = state_dict["critical_point"]
    elif abs_rel_err(P, Pvp) < delta:
        state = state_dict["VL_equi"]
    elif P >= Pvp + delta:
        state = state_dict["liq"]
    elif P <= Pvp - delta:
        state = state_dict["vap"]
    else:
        raise ValueError("Couldn't identify fluid state.")

    return state


# ideal gas properties


def return_Cp(T, a0, a1, a2, a3, a4, Tmin, Tmax):
    """
    Cp/R_IG = a0 + a1*T + a2*T**2 + a3*T**3 + a4*T**4
    :param T: temperature, K
    :param a0, a1, a2, a3, a4: constants
    :return: Cp_IG, J mol-1 K-1
    """
    cp = namedtuple("Cp", ["Cp", "msg"])
    msg = None
    if Tmin is None and Tmax is None:
        msg = "no temperature range given"
    elif T < Tmin:
        msg = "T < Tmin, range = [{0:.3e}, {1:.3e}] K".format(Tmin, Tmax)
    elif T > Tmax:
        msg = "T > Tmax, range = [{0:.3e}, {1:.3e}] K".format(Tmin, Tmax)
    ans = R_IG * (a0 + a1 * T + a2 * T ** 2 + a3 * T ** 3 + a4 * T ** 4)
    ans = cp(ans, msg)
    return ans


def return_Cv(T, a0, a1, a2, a3, a4, Tmin, Tmax):
    return return_Cp(T, a0, a1, a2, a3, a4, Tmin, Tmax).Cp - R_IG


# @jit(nopython=True, cache=True)
def return_deltaH_IG(T1, T2, a0, a1, a2, a3, a4):
    ans = R_IG * (
        a0 * (T2 - T1)
        + (T2 ** 2 - T1 ** 2) * a1 / 2
        + (T2 ** 3 - T1 ** 3) * a2 / 3
        + (T2 ** 4 - T1 ** 4) * a3 / 4
        + (T2 ** 5 - T1 ** 5) * a4 / 5
    )
    return ans


# @jit(nopython=True, cache=True)
def return_deltaS_IG(T1, T2, P1, P2, a0, a1, a2, a3, a4):
    ans = (
        R_IG
        * (
            -3 * T1 ** 4 * a4
            - 4 * T1 ** 3 * a3
            - 6 * T1 ** 2 * a2
            - 12 * T1 * a1
            + 3 * T2 ** 4 * a4
            + 4 * T2 ** 3 * a3
            + 6 * T2 ** 2 * a2
            + 12 * T2 * a1
            - 12 * a0 * np.log(T1)
            + 12 * a0 * np.log(T2)
            - 12 * np.log(P2 / P1)
        )
        / 12
    )
    return ans


# @jit(nopython=True, cache=True)
def return_deltaG_IG(dH, T, dS):
    return dH - T * dS


# @jit(nopython=True, cache=True)
def return_deltaU_IG(dH, T1, T2):
    return dH - (T2 - T1) * R_IG


# @jit(nopython=True, cache=True)
def return_deltaA_IG(dU, T, dS):
    return dU - T * dS


# @jit(nopython=True, cache=True)
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
    dU_IG = return_deltaU_IG(dH_IG, Tref, T)
    dA_IG = return_deltaA_IG(dU_IG, T, dS_IG)

    dict_ans = {
        "Cp_IG": Cp_IG,
        "dH_IG": dH_IG,
        "dS_IG": dS_IG,
        "dG_IG": dG_IG,
        "dU_IG": dU_IG,
        "dA_IG": dA_IG,
        "msg": msg,
    }
    return dict_ans
