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


class biPR1976(BiBehavior):
    def getBi(self, i: int, T: float, substances) -> float:
        return 0.07780 / (substances[i].Pc / (R_IG * substances[i].Tc))


class thetaiPR1976(ThetaiBehavior):
    def a(self, i: int, T: float, substances):
        return 0.45724 * np.power(R_IG * substances[i].Tc, 2) / substances[i].Pc

    def m(self, i: int, T: float, substances):
        w = substances[i].omega
        return 0.37464 + 1.54226 * w - 0.26992 * w * w

    def alpha(self, i: int, T: float, substances):
        _m = self.m(i, T, substances)
        return np.power(1.0 + _m * (1.0 - np.sqrt(T / substances[i].Tc)), 2)

    def getThetai(self, i: int, T: float, substances) -> float:
        return self.alpha(i, T, substances) * self.a(i, T, substances)


class deltaMixPR1976(DeltaMixtureRuleBehavior):
    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return 2.0 * bmb.bm(y, T, bib, substances)

    def diffDeltam(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return 2.0 * bmb.diffBm(i, y, T, bib, substances)


class epsilonMixPR1976(EpsilonMixtureRuleBehavior):
    def epsilonm(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return -(bmb.bm(y, T, bib, substances)) ** 2

    def diffEpsilonm(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return (
            -2.0 * bmb.bm(y, T, bib, substances) * bmb.diffBm(i, y, T, bib, substances)
        )


class PR1976(EOSMixture):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Peng and Robinson (1976)"
        self.mixRuleBehavior = ClassicMixtureRule()
        self.biBehavior = biPR1976()
        self.thetaiBehavior = thetaiPR1976()
        self.deltaMixBehavior = deltaMixPR1976()
        self.epsilonMixBehavior = epsilonMixPR1976()
