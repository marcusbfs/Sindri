import numpy as np
import IdealGasPropertiesPureSubstance as IGP
from constants import R_IG
from scipy.integrate import quad


def return_MixCp_IG(T, y, a0, a1, a2, a3, a4, Tmin, Tmax):
    Cpmix = 0
    msgs = []
    # TODO what if a0 = None for a compound?
    for _y, _a0, _a1, _a2, _a3, _a4, _Tmin, _Tmax in zip(
        y, a0, a1, a2, a3, a4, Tmin, Tmax
    ):
        Cpi = IGP.return_Cp(T, _a0, _a1, _a2, _a3, _a4, _Tmin, _Tmax)
        Cpmix += _y * Cpi.Cp
        msgs.append(Cpi.msg)

    return Cpmix, msgs


def return_MixH_IG(T1, T2, y, a0, a1, a2, a3, a4):

    ans = np.sum(
        y
        * R_IG
        * (
            a0 * (T2 - T1)
            + (T2 ** 2 - T1 ** 2) * a1 / 2
            + (T2 ** 3 - T1 ** 3) * a2 / 3
            + (T2 ** 4 - T1 ** 4) * a3 / 4
            + (T2 ** 5 - T1 ** 5) * a4 / 5
        )
    )
    return ans


def return_MixU_IG(dH, y, T1, T2):
    _sum = np.sum(y * (T2 - T1) * R_IG)
    return dH - _sum


def return_MixS_IG(T1, T2, P1, P2, y, a0, a1, a2, a3, a4):
    ans = np.sum(
        y
        * (
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
    )
    sum2 = np.sum(y * np.log(y))
    ret = ans - R_IG * sum2
    return ret


def return_MixG_IG(dH, T, dS):
    return dH - T * dS


def return_MixA_IG(dU, T, dS):
    return dU - T * dS


def return_MixIdealGasProperties(Tref, T, Pref, P, y, a0, a1, a2, a3, a4, Tmin, Tmax):
    Cp_IG, msg = return_MixCp_IG(T, y, a0, a1, a2, a3, a4, Tmin, Tmax)
    dH_IG = return_MixH_IG(Tref, T, y, a0, a1, a2, a3, a4)
    dS_IG = return_MixS_IG(Tref, T, Pref, P, y, a0, a1, a2, a3, a4)
    dU_IG = return_MixU_IG(dH_IG, y, Tref, T)
    dG_IG = return_MixG_IG(dH_IG, T, dS_IG)
    dA_IG = return_MixA_IG(dU_IG, T, dS_IG)

    dict_ans = {
        "p": Cp_IG,
        "H": dH_IG,
        "S": dS_IG,
        "G": dG_IG,
        "U": dU_IG,
        "A": dA_IG,
        "msg": msg,
    }
    return dict_ans
