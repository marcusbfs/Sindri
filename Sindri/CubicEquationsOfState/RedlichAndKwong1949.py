import numpy as np

from EOSMixture import EOSMixture
from EOSParametersBehavior.ParametersBehaviorInterface import (
    DeltaiBehavior,
    EpsiloniBehavior,
)
from MixtureRules.ClassicMixtureRule import ClassicMixtureRule
from MixtureRules.MixtureRulesInterface import (
    BiBehavior,
    ThetaiBehavior,
    DeltaMixtureRuleBehavior,
    EpsilonMixtureRuleBehavior,
    BMixtureRuleBehavior,
)
from constants import R_IG


class biRK1949(BiBehavior):
    def getBi(self, i: int, T: float, substances) -> float:
        return 0.08664 / (substances[i].Pc / (R_IG * substances[i].Tc))


class thetaiRK1949(ThetaiBehavior):
    def a(self, i: int, T: float, substances):
        return 0.42748 * (R_IG * substances[i].Tc) ** 2 / substances[i].Pc

    def alpha(self, i: int, T: float, substances):
        return 1.0 / np.sqrt(T / substances[i].Tc)

    def getThetai(self, i: int, T: float, substances) -> float:
        _alpha = self.alpha(i, T, substances)
        return _alpha * self.a(i, T, substances)


class epsiloniRK1949(EpsiloniBehavior):
    def getEpsiloni(self, b: float) -> float:
        return 0.0


class deltaiRK1949(DeltaiBehavior):
    def getDeltai(self, b: float) -> float:
        return b


class deltaMixRK1949(DeltaMixtureRuleBehavior):
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


class epsilonMixRK1949(EpsilonMixtureRuleBehavior):
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


class RedlichAndKwong1949(EOSMixture):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Redlich and Kwong (1949)"
        self.mixRuleBehavior = ClassicMixtureRule()
        self.biBehavior = biRK1949()
        self.thetaiBehavior = thetaiRK1949()
        self.deltaiBehavior = deltaiRK1949()
        self.epsiloniBehavior = epsiloniRK1949()
        self.deltaMixBehavior = deltaMixRK1949()
        self.epsilonMixBehavior = epsilonMixRK1949()
