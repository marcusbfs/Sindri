from MixtureRules.MixtureRulesInterface import (
    BiBehavior,
    ThetaiBehavior,
    DeltaiBehavior,
    DeltaMixtureRuleBehavior,
    EpsiloniBehavior,
    EpsilonMixtureRuleBehavior,
    BMixtureRuleBehavior,
    ThetaMixtureRuleBehavior,
)
import numpy as np
from constants import R_IG
from EOSMixture import EOSMixture
from MixtureRules.ClassicMixtureRule import ClassicMixtureRule


class biWilson1964(BiBehavior):
    def getBi(self, i: int, T: float, substances) -> float:
        return 0.08664 / (substances[i].Pc / (R_IG * substances[i].Tc))


class thetaiWilson1964(ThetaiBehavior):
    def a(self, i: int, T: float, substances):
        return 0.42748 * (R_IG * substances[i].Tc) ** 2 / substances[i].Pc

    def alpha(self, i: int, T: float, substances):
        tr = T / substances[i].Tc
        w = substances[i].omega
        return (1.0 + (1.57 + 1.62 * w) * (1.0 / tr - 1.0)) * tr

    def getThetai(self, i: int, T: float, substances) -> float:
        _alpha = self.alpha(i, T, substances)
        return _alpha * self.a(i, T, substances)


class epsiloniWilson1964(EpsiloniBehavior):
    def getEpsiloni(self, b: float) -> float:
        return 0.0


class deltaiWilson1964(DeltaiBehavior):
    def getDeltai(self, b: float) -> float:
        return b


class deltaMixWilson1964(DeltaMixtureRuleBehavior):
    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: BMixtureRuleBehavior, substances
    ) -> float:
        return bmb.bm(y, T, bib, substances)

    def diffDeltam(
        self,
        i: int,
        y,
        T: float,
        bib: BiBehavior,
        bmb: BMixtureRuleBehavior,
        substances,
    ) -> float:
        return bmb.diffBm(i, y, T, bib, substances)


class epsilonMixWilson1964(EpsilonMixtureRuleBehavior):
    def epsilonm(
        self, y, T: float, bib: BiBehavior, bmb: BMixtureRuleBehavior, substances
    ) -> float:
        return 0.0

    def diffEpsilonm(
        self,
        i: int,
        y,
        T: float,
        bib: BiBehavior,
        bmb: BMixtureRuleBehavior,
        substances,
    ) -> float:
        return 0.0


class Wilson1964(EOSMixture):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Wilson (1964)"
        self.mixRuleBehavior = ClassicMixtureRule()
        self.biBehavior = biWilson1964()
        self.thetaiBehavior = thetaiWilson1964()
        self.deltaiBehavior = deltaiWilson1964()
        self.epsiloniBehavior = epsiloniWilson1964()
        self.deltaMixBehavior = deltaMixWilson1964()
        self.epsilonMixBehavior = epsilonMixWilson1964()
