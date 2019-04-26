from typing import List

import numpy as np
from numba import njit, float64

import db
from Properties import DeltaProp, VaporPressure
from constants import R_IG, DBL_EPSILON

state_dict = {
    # It must have the following order:
    #   supercritical, critical point, vapor-liquid equi., liquid, vapor.
    "supercritical": "supercritical fluid",
    "critical_point": "critical point",
    "VL_equi": "vapor-liquid equilibrium",
    "liq": "compressed or unsaturated liquid",
    "vap": "superheated steam",
}


class SubstanceProp(object):
    def __init__(self, name: str, formula: str):

        db.init()

        table_name = "v_all_properties_including_correlations"
        query = (
            "SELECT * FROM "
            + table_name
            + " WHERE Formula LIKE '%"
            + formula
            + "%'"
            + " AND Name LIKE '%"
            + name
            + "%'"
        )
        db.cursor.execute(query)
        results = db.cursor.fetchall()[0]

        self.Formula = self._ifString(results[0])
        self.Name = self._ifString(results[1])
        self.CAS = self._ifString(results[2])

        self.MolWt = self._ifNumber(results[3])
        self.Tfp = self._ifNumber(results[4])
        self.Tb = self._ifNumber(results[5])

        self.Tc = self._ifNumber(results[6])
        self.Pc = self._ifNumber(results[7]) * 1e5
        self.Vc = self._ifNumber(results[8]) / 100 ** 3
        self.Zc = self._ifNumber(results[9])
        self.omega = self._ifNumber(results[10])

        try:
            tcps = results[11].split("-")
            tcpmin, tcpmax = tcps[0], tcps[1]
        except:
            tcpmin, tcpmax = 0.0, 0.0

        self.Tcpmin, self.Tcpmax = self._ifNumber(tcpmin), self._ifNumber(tcpmax)

        self.a0 = self._ifNumber(results[12])
        self.a1 = self._ifNumber(results[13])
        self.a2 = self._ifNumber(results[14])
        self.a3 = self._ifNumber(results[15])
        self.a4 = self._ifNumber(results[16])

        self.CpIG, self.CpLiq = self._ifNumber(results[17]), self._ifNumber(results[18])

        self.Ant_A = self._ifNumber(results[19])
        self.Ant_B = self._ifNumber(results[20])
        self.Ant_C = self._ifNumber(results[21])

        self.Pvmin = self._ifNumber(results[22]) * 1e5
        self.Tvmin = self._ifNumber(results[23])
        self.Pvmax = self._ifNumber(results[24]) * 1e5
        self.Tvmax = self._ifNumber(results[25])

        self._no_cp_err = "Substance {} doesn't have Cp parameters".format(self.Name)

        self.substance_id = int(
            db.cursor.execute(
                "SELECT substance_id from substance "
                + " WHERE formula LIKE '%"
                + formula
                + "%'"
                + " AND name LIKE '%"
                + name
                + "%'"
            ).fetchone()[0]
        )

    def getSubstanceID(self):
        return self.substance_id

    def getIGProps(self, Tref: float, T: float, Pref: float, P: float):
        if self.hasCp():
            cp = self.getCp(T)
            h = self.getH(Tref, T)
            s = self.getS(Tref, T, Pref, P)
            g = self.getG(Tref, T, Pref, P)
            u = self.getU(Tref, T)
            a = self.getA(Tref, T, Pref, P)
            return DeltaProp(cp, h, s, g, u, a)
        else:
            raise ValueError(self._no_cp_err)

    def getCp(self, T: float) -> float:
        if self.hasCp():
            return R_IG * (
                self.a0
                + self.a1 * T
                + self.a2 * T ** 2
                + self.a3 * T ** 3
                + self.a4 * T ** 4
            )
        else:
            raise ValueError(self._no_cp_err)

    def getH(self, Tref: float, T: float) -> float:
        if self.hasCp():
            return _getH_helper(Tref, T, self.a0, self.a1, self.a2, self.a3, self.a4)
        else:
            raise ValueError(self._no_cp_err)

    def getS(self, Tref: float, T: float, Pref: float, P: float) -> float:
        if self.hasCp():
            return _getS_helper(
                Tref, T, Pref, P, self.a0, self.a1, self.a2, self.a3, self.a4
            )
        else:
            raise ValueError(self._no_cp_err)

    def getU(self, Tref: float, T: float) -> float:
        if self.hasCp():
            return self.getH(Tref, T) - (T - Tref) * R_IG
        else:
            raise ValueError(self._no_cp_err)

    def getG(self, Tref: float, T: float, Pref: float, P: float) -> float:
        if self.hasCp():
            return self.getH(Tref, T) - T * self.getS(Tref, T, Pref, P)
        else:
            raise ValueError(self._no_cp_err)

    def getA(self, Tref: float, T: float, Pref: float, P: float) -> float:
        if self.hasCp():
            return self.getU(Tref, T) - T * self.getS(Tref, T, Pref, P)
        else:
            raise ValueError(self._no_cp_err)

    def getCpLog(self, Tref: float, T: float) -> str:
        log = ""
        if not self.checkCpRange(Tref):
            log += "WARNING {} Tref out of Cp range: [{:.3f}, {:.3f}]\n".format(
                self.Name, self.Tcpmin, self.Tcpmax
            )
        if not self.checkCpRange(T):
            log += "WARNING {} T out of Cp range: [{:.3f}, {:.3f}]\n".format(
                self.Name, self.Tcpmin, self.Tcpmax
            )
        return log

    def hasAntoine(self) -> bool:
        if self.Ant_A != 0 and self.Ant_B != 0 and self.Ant_C != 0:
            return True
        return False

    def getPvpAntoine(self, T: float) -> float:
        if self.hasAntoine():
            return _getPvpAntoine_helper(T, self.Ant_A, self.Ant_B, self.Ant_C)
        else:
            return 0.0

    def getAntoineTsat(self, P: float) -> float:
        tsat = 273.15 - self.Ant_C + self.Ant_B / (self.Ant_A - np.log10(P * 1e-5))
        return tsat

    def checkAntoineRange(self, T: float) -> bool:
        if self.Tvmin <= T <= self.Tvmax:
            return True
        return False

    def getAntoineLog(self, T: float) -> str:
        log = ""
        if not self.checkAntoineRange(T):
            log += "T out of Antoine range: [{}, {}]\n".format(self.Tvmin, self.Tvmax)
        return log

    def getPvpAW(self, T: float) -> float:
        if self.Pc != 0 and self.Tc != 0 and self.omega != 0:

            return _ambroseWaltonVP_helper(self.Pc, T / self.Tc, self.omega)
        return 0.0

    def getPvpLK(self, T: float) -> float:
        if self.Pc != 0 and self.Tc != 0 and self.omega != 0:

            return _leeKeslerVP_helper(self.Pc, T / self.Tc, self.omega)
        return 0.0

    # will this function work for mixtures? (applying the necessaries
    def getFluidState(self, P: float, T: float, eq, delta=1e-3):
        pvpaw = self.getPvpAW(T)
        Pvp = eq.getPvp(T, pvpaw)[0]

        Pr = P / self.Pc
        Tr = T / self.Tc

        def _relError(x, y):
            if abs(x) < DBL_EPSILON:
                return x - y
            return (x - y) / x

        if Tr > 1 or Pr > 1:
            state = state_dict["supercritical"]
        elif (Tr > 0.9 and Tr < 1.1) and (Pr > 0.9 and Pr < 1.1):
            state = state_dict["critical_point"]
        elif np.abs(_relError(P, Pvp)) < delta:
            state = state_dict["VL_equi"]
        elif P >= Pvp + delta:
            state = state_dict["liq"]
        elif P <= Pvp - delta:
            state = state_dict["vap"]
        else:
            raise ValueError("Couldn't identify fluid state.")
        return state

    def getPvps(self, T: float) -> VaporPressure:
        pvp = VaporPressure()
        aw = self.getPvpAW(T)
        lk = self.getPvpLK(T)
        ant = self.getPvpAntoine(T)
        if aw:
            pvp.setAW(aw)
        if lk:
            pvp.setLK(lk)
        if ant:
            pvp.setAntoine(ant, self.getAntoineLog(T))
        return pvp

    def checkCpRange(self, T: float) -> bool:
        if self.Tcpmin <= T <= self.Tcpmax:
            return True
        return False

    def hasCp(self) -> bool:
        if self.a0 != 0:

            return True
        return False

    def _ifString(self, s: str, ret="") -> str:
        if isinstance(s, str) and len(s) > 0:
            return s
        return ret

    def _ifNumber(self, n, ret=0) -> float:
        try:
            float(n) * 1.0 + 1.0
            return float(n)
        except:
            return ret


class MixtureProp(object):
    def __init__(self, mix: List[SubstanceProp], y: List[float]):
        self.substances = np.atleast_1d(mix)
        self.y = np.atleast_1d(y)
        assert len(self.substances) == len(self.y)
        assert np.sum(self.y) == 1.0
        self.n = len(mix)

    def getIGProps(self, Tref: float, T: float, Pref: float, P: float) -> DeltaProp:
        if self.hasCp():
            cp = self.getCp(T)
            h = self.getH(Tref, T)
            s = self.getS(Tref, T, Pref, P)
            g = self.getG(Tref, T, Pref, P)
            u = self.getU(Tref, T)
            a = self.getA(Tref, T, Pref, P)
            return DeltaProp(cp, h, s, g, u, a)
        else:
            raise ValueError("Mixture has no Cp")

    def hasCp(self) -> bool:
        for subs in self.substances:
            if not subs.hasCp():
                return False
        return True

    def getCp(self, T: float) -> float:
        if self.hasCp():
            sum1 = 0
            for i in range(self.n):
                sum1 += self.y[i] * self.substances[i].getCp(T)
            return sum1
        return 0

    def getH(self, Tref: float, T: float) -> float:
        if self.hasCp():
            sum1 = 0
            for i in range(self.n):
                sum1 += self.y[i] * self.substances[i].getH(Tref, T)
            return sum1
        return 0

    def getS(self, Tref: float, T: float, Pref: float, P: float) -> float:
        if self.hasCp():
            if self.n == 1:
                return self.substances[0].getS(Tref, T, Pref, P)
            sum1 = 0
            sum2 = 0
            for i in range(self.n):
                sum1 += self.y[i] * self.substances[i].getS(Tref, T, Pref, P)
                sum2 += self.y[i] * np.log(self.y[i])
            return sum1 - R_IG * sum2
        return 0

    def getU(self, Tref: float, T: float) -> float:
        if self.hasCp():
            sum1 = 0
            for i in range(self.n):
                sum1 += self.y[i] * self.substances[i].getU(Tref, T)
            return sum1
        return 0

    def getG(self, Tref: float, T: float, Pref: float, P: float) -> float:
        if self.hasCp():
            if self.n == 1:
                return self.substances[0].getG(Tref, T, Pref, P)
            return self.getH(Tref, T) - T * self.getS(Tref, T, Pref, P)
        return 0

    def getA(self, Tref: float, T: float, Pref: float, P: float) -> float:
        if self.hasCp():
            if self.n == 1:
                return self.substances[0].getA(Tref, T, Pref, P)
            return self.getU(Tref, T) - T * self.getS(Tref, T, Pref, P)
        return 0

    def checkCpRange(self, T: float) -> bool:
        if self.hasCp():
            for subs in self.substances:

                if not subs.checkCpRange(T):
                    return False
            return True
        else:
            return False

    def getCpLog(self, Tref: float, T: float) -> str:
        log = ""
        for subs in self.substances:
            log += subs.getCpLog(Tref, T)
        return log

    def getMolWt(self) -> float:
        m = 0
        for i in range(self.n):
            if self.substances[i].MolWt != 0:
                m += self.y[i] * self.substances[i].MolWt
            else:
                return 0
        return m


# ============ helper functions (for performance) =================


@njit(
    float64(float64, float64, float64, float64, float64, float64, float64), cache=True
)
def _getH_helper(Tref: float, T: float, a0, a1, a2, a3, a4) -> float:
    return R_IG * (
        a0 * (T - Tref)
        + (T ** 2 - Tref ** 2) * a1 / 2
        + (T ** 3 - Tref ** 3) * a2 / 3
        + (T ** 4 - Tref ** 4) * a3 / 4
        + (T ** 5 - Tref ** 5) * a4 / 5
    )


@njit(float64(float64, float64, float64, float64), cache=True)
def _getPvpAntoine_helper(T, Ant_A, Ant_B, Ant_C):
    ans = 10 ** (Ant_A - Ant_B / (T + Ant_C - 273.15))
    P = ans * 1e5
    return P


@njit(
    float64(
        float64, float64, float64, float64, float64, float64, float64, float64, float64
    ),
    cache=True,
)
def _getS_helper(
    Tref: float, T: float, Pref: float, P: float, a0, a1, a2, a3, a4
) -> float:
    return (
        R_IG
        * (
            -3 * Tref ** 4 * a4
            - 4 * Tref ** 3 * a3
            - 6 * Tref ** 2 * a2
            - 12 * Tref * a1
            + 3 * T ** 4 * a4
            + 4 * T ** 3 * a3
            + 6 * T ** 2 * a2
            + 12 * T * a1
            - 12 * a0 * np.log(Tref)
            + 12 * a0 * np.log(T)
            - 12 * np.log(P / Pref)
        )
        / 12
    )


@njit(float64(float64, float64, float64), cache=True)
def _ambroseWaltonVP_helper(Pc, Tr, omega):
    """ Ambrose-Walton (1989) correlation for estimating the vapor pressure.

    Parameters
    ----------
    Pc : float
        Critical pressure, in Pascal.
    Tr : float
        Reduced temperature, adimensional.
    omega : float
        Acentric factor, adimensinoal.

    Returns
    -------
    Pvp : float
        The estimated vapor pressure at T = Tc * Tr. The pressure is given in Pascal.

    """
    tau = 1.0 - Tr
    f0 = (
        -5.97616 * tau
        + 1.29874 * tau ** 1.5
        - 0.60394 * tau ** 2.5
        - 1.06841 * tau ** 5
    ) / Tr
    f1 = (
        -5.03365 * tau
        + 1.11505 * tau ** 1.5
        - 5.41217 * tau ** 2.5
        - 7.46628 * tau ** 5
    ) / Tr
    f2 = (
        -0.64771 * tau
        + 2.41539 * tau ** 1.5
        - 4.26979 * tau ** 2.5
        - 3.25259 * tau ** 5
    ) / Tr
    Pvpr = np.exp(f0 + omega * f1 + f2 * omega ** 2)
    Pvp = Pvpr * Pc
    return Pvp


@njit(float64(float64, float64, float64), cache=True)
def _leeKeslerVP_helper(Pc, Tr, omega):
    """ Lee-Kesler correlation for estimating the vapor pressure.

    Parameters
    ----------
    Pc : float
        Critical pressure, in Pascal.
    Tr : float
        Reduced temperature, adimensional.
    omega : float
        Acentric factor, adimensinoal.

    Returns
    -------
    Pvp : float
        The estimated vapor pressure at T = Tc * Tr. The pressure is given in Pascal.

    """
    f0 = 5.92714 - 6.09648 / Tr - 1.28862 * np.log(Tr) + 0.169347 * Tr ** 6
    f1 = 15.2518 - 15.6878 / Tr - 13.4721 * np.log(Tr) + 0.43677 * Tr ** 6
    Pvpr = np.exp(f0 + omega * f1)
    Pvp = Pvpr * Pc
    return Pvp
