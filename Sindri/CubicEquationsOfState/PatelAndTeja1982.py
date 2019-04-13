import numpy as np

from EOSMixture import EOSMixture
from MixtureRules.ClassicMixtureRule import ClassicMixtureRule
from MixtureRules.MixtureRulesInterface import (
    BiBehavior,
    ThetaiBehavior,
    DeltaMixtureRuleBehavior,
    EpsilonMixtureRuleBehavior,
    MixtureRuleBehavior,
)
from constants import R_IG
from polyEqSolver import solve_cubic


def _calc_a_b_c(i: int, T: float, substances):
    w = substances[i].omega
    Pc = substances[i].Pc
    Tc = substances[i].Tc
    zeta_c = 0.32903 - 0.076799 * w + 0.0211947 * w ** 2
    omega_c = 1.0 - 3.0 * zeta_c
    c = omega_c * R_IG * Tc / Pc
    r = np.atleast_1d(solve_cubic(1, 2 - 3 * zeta_c, 3 * zeta_c ** 2, -zeta_c ** 3))
    omega_b = np.min(r[r >= 0])
    omega_a = (
        3 * zeta_c ** 2 + 3 * (1 - 2 * zeta_c) * omega_b + omega_b ** 2 + 1 - 3 * zeta_c
    )
    a = omega_a * (R_IG * Tc) ** 2 / Pc
    b = omega_b * (R_IG * Tc) / Pc
    return a, b, c


class biPT1982(BiBehavior):
    def getBi(self, i: int, T: float, substances) -> float:
        a, b, c = _calc_a_b_c(i, T, substances)
        return b


class thetaiPT1982(ThetaiBehavior):
    def a(self, i: int, T: float, substances):
        a, b, c = _calc_a_b_c(i, T, substances)
        return a

    def m(self, i: int, T: float, substances):
        w = substances[i].omega
        F = 0.45241 + 1.30982 * w - 0.295937 * w ** 2
        return F

    def alpha(self, i: int, T: float, substances):
        _m = self.m(i, T, substances)
        return np.power(1.0 + _m * (1.0 - np.sqrt(T / substances[i].Tc)), 2)

    def getThetai(self, i: int, T: float, substances) -> float:
        _alpha = self.alpha(i, T, substances)
        return _alpha * self.a(i, T, substances)


class CBehavior:
    def getCi(self, i: int, T: float, substances):
        a, b, c = _calc_a_b_c(i, T, substances)
        return c

    def getCm(self, y, T: float, substances):
        s = 0.0
        for i in range(len(y)):
            c = self.getCi(i, T, substances)
            s += c * y[i]
        return s

    def getDiffCm(self, i: int, y, T: float, substances):
        return self.getCi(i, T, substances)


class deltaMixPT1982(DeltaMixtureRuleBehavior):
    def __init__(self):
        self.c = CBehavior()

    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        c = self.c.getCm(y, T, substances)
        b = bmb.bm(y, T, bib, substances)
        return c + b

    def diffDeltam(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        cline = self.c.getDiffCm(i, y, T, substances)
        bline = bmb.diffBm(i, y, T, bib, substances)
        return cline + bline


class epsilonMixPT1982(EpsilonMixtureRuleBehavior):
    def __init__(self):
        self.c = CBehavior()

    def epsilonm(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        c = self.c.getCm(y, T, substances)
        b = bmb.bm(y, T, bib, substances)
        return -b * c

    def diffEpsilonm(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        c = self.c.getCm(y, T, substances)
        cline = self.c.getDiffCm(i, y, T, substances)
        b = bmb.bm(y, T, bib, substances)
        bline = bmb.diffBm(i, y, T, bib, substances)
        return -bline * c - cline * b


class PT1982(EOSMixture):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Patel and Teja (1982)"
        self.mixRuleBehavior = ClassicMixtureRule()
        self.biBehavior = biPT1982()
        self.thetaiBehavior = thetaiPT1982()
        self.deltaMixBehavior = deltaMixPT1982()
        self.epsilonMixBehavior = epsilonMixPT1982()
