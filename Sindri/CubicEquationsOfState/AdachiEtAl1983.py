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


class biAdachi1983(BiBehavior):
    def getBi(self, i: int, T: float, substances) -> float:
        w = substances[i].omega
        B1 = 0.08974 + w * (-0.03452 + w * 0.0033)
        return B1 * R_IG * substances[i].Tc / substances[i].Pc


class thetaiAdachi1983(ThetaiBehavior):
    def a(self, i: int, T: float, substances):
        w = substances[i].omega
        A = 0.44869 + w * (0.04024 + w * (0.01111 - w * 0.00576))
        return A * (R_IG * substances[i].Tc) ** 2 / substances[i].Pc

    def m(self, i: int, T: float, substances):
        w = substances[i].omega
        return 0.4070 + w * (1.3787 - w * 0.2933)

    def alpha(self, i: int, T: float, substances):
        _m = self.m(i, T, substances)
        return np.power(1.0 + _m * (1.0 - np.sqrt(T / substances[i].Tc)), 2)

    def getThetai(self, i: int, T: float, substances) -> float:
        _alpha = self.alpha(i, T, substances)
        return _alpha * self.a(i, T, substances)


def _calcB2(i: int, T: float, substances):
    w = substances[i].omega
    B2 = 0.03686 + w * (0.00405 + w * (-0.01073 + w * 0.00157))
    return B2 * R_IG * substances[i].Tc / substances[i].Pc


def _calcB2mix(y, T: float, substances):
    s = 0.0
    for i in range(len(y)):
        s += y[i] * _calcB2(i, T, substances)
    return s


def _calcB3(i: int, T: float, substances):
    w = substances[i].omega
    B3 = 0.15400 + w * (0.14122 + w * (-0.00272 - w * 0.00484))
    return B3 * R_IG * substances[i].Tc / substances[i].Pc


def _calcB3mix(y, T: float, substances):
    s = 0.0
    for i in range(len(y)):
        s += y[i] * _calcB3(i, T, substances)
    return s


class deltaMixAdachi1983(DeltaMixtureRuleBehavior):
    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        B2mix = _calcB2mix(y, T, substances)
        B3mix = _calcB3mix(y, T, substances)
        return B3mix - B2mix

    def diffDeltam(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return _calcB3(i, T, substances) - _calcB2(i, T, substances)


class epsilonMixAdachi1983(EpsilonMixtureRuleBehavior):
    def epsilonm(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        B2mix = _calcB2mix(y, T, substances)
        B3mix = _calcB3mix(y, T, substances)
        return -B2mix * B3mix

    def diffEpsilonm(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        B2mix = _calcB2mix(y, T, substances)
        B3mix = _calcB3mix(y, T, substances)
        B2line = _calcB2(i, T, substances)
        B3line = _calcB3(i, T, substances)
        return -B2line * B3mix - B3line * B2mix


class Adachi1983(EOSMixture):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Adachi, et al. (1983)"
        self.mixRuleBehavior = ClassicMixtureRule()
        self.biBehavior = biAdachi1983()
        self.thetaiBehavior = thetaiAdachi1983()
        self.deltaMixBehavior = deltaMixAdachi1983()
        self.epsilonMixBehavior = epsilonMixAdachi1983()
