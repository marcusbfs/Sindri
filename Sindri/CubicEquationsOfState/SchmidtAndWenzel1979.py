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


# TODO


def _calc_a_and_b(T: float, Tc: float, Pc: float, w: float):
    Bc = 0.25989 + w * (-0.0217 + 0.00375 * w)
    bs = solve_cubic(6.0 * w + 1.0, 3.0, 3.0, -1.0, x0=Bc)
    Bc = np.min([x for x in bs if x > 0])
    zeta_c = 1.0 / (3.0 * (1.0 + w * Bc))
    omega_b = Bc * zeta_c
    omega_a = (1.0 - zeta_c * (1.0 - Bc)) ** 3
    b = omega_b * R_IG * Tc / Pc
    a = omega_a * (R_IG * Tc) ** 2 / Pc
    return a, b


class biSW1979(BiBehavior):
    def getBi(self, i: int, T: float, substances) -> float:
        a, b = _calc_a_and_b(T, substances[i].Tc, substances[i].Pc, substances[i].omega)
        return b


class thetaiSW1979(ThetaiBehavior):
    def m(self, i: int, T: float, substances):
        w = substances[i].omega
        tr = T / substances[i].Tc
        k0 = 0.465 + w * (1.347 - 0.528 * w)
        if tr > 1:
            tr = 1.0
        k = k0 + (5.0 * tr - 3.0 * k0 - 1.0) ** 2 / 70.0
        return k

    def a(self, i: int, T: float, substances):
        a, b = _calc_a_and_b(T, substances[i].Tc, substances[i].Pc, substances[i].omega)
        return a

    def alpha(self, i: int, T: float, substances):
        _m = self.m(i, T, substances)
        return np.power(1.0 + _m * (1.0 - np.sqrt(T / substances[i].Tc)), 2)

    def getThetai(self, i: int, T: float, substances) -> float:
        _alpha = self.alpha(i, T, substances)
        return _alpha * self.a(i, T, substances)


def getW(y, substances):
    s = 0.0
    for i in range(len(y)):
        s += substances[i].omega * y[i]
    return -3.0 * s


class deltaMixSW1979(DeltaMixtureRuleBehavior):
    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        u = 1.0 - getW(y, substances)
        return u * bmb.bm(y, T, bib, substances)

    def diffDeltam(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        u = 1.0 - getW(y, substances)
        return (
            u * bmb.diffBm(i, y, T, bib, substances)
            - bmb.bm(y, T, bib, substances) * substances[i].omega
        )


class epsilonMixSW1979(EpsilonMixtureRuleBehavior):
    def epsilonm(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        w = getW(y, substances)
        return w * (bmb.bm(y, T, bib, substances)) ** 2

    def diffEpsilonm(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        w = getW(y, substances)
        diffw = substances[i].omega
        b = bmb.bm(y, T, bib, substances)
        diffb = bmb.diffBm(i, y, T, bib, substances)
        return diffw * b * b + w * 2.0 * b * diffb


class SW1979(EOSMixture):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Schmidt and Wenzel (1979)"
        self.mixRuleBehavior = ClassicMixtureRule()
        self.biBehavior = biSW1979()
        self.thetaiBehavior = thetaiSW1979()
        self.deltaMixBehavior = deltaMixSW1979()
        self.epsilonMixBehavior = epsilonMixSW1979()
