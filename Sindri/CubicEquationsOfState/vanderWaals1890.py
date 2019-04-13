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


class bivanderWaals1890(BiBehavior):
    def getBi(self, i: int, T: float, substances) -> float:
        return 0.125 / (substances[i].Pc / (R_IG * substances[i].Tc))


class thetaivanderWaals1890(ThetaiBehavior):
    def a(self, i: int, T: float, substances):
        return 0.421875 * (R_IG * substances[i].Tc) ** 2 / substances[i].Pc

    def getThetai(self, i: int, T: float, substances) -> float:
        return self.a(i, T, substances)


class epsilonivanderWaals1890(EpsiloniBehavior):
    def getEpsiloni(self, b: float) -> float:
        return 0.0


class deltaivanderWaals1890(DeltaiBehavior):
    def getDeltai(self, b: float) -> float:
        return 0.0


class deltaMixvanderWaals1890(DeltaMixtureRuleBehavior):
    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: BMixtureRuleBehavior, substances
    ) -> float:
        return 0.0

    def diffDeltam(
        self,
        i: int,
        y,
        T: float,
        bib: BiBehavior,
        bmb: BMixtureRuleBehavior,
        substances,
    ) -> float:
        return 0.0


class epsilonMixvanderWaals1890(EpsilonMixtureRuleBehavior):
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


class vanderWaals1890(EOSMixture):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "van der Waals (1890)"
        self.mixRuleBehavior = ClassicMixtureRule()
        self.biBehavior = bivanderWaals1890()
        self.thetaiBehavior = thetaivanderWaals1890()
        self.deltaiBehavior = deltaivanderWaals1890()
        self.epsiloniBehavior = epsilonivanderWaals1890()
        self.deltaMixBehavior = deltaMixvanderWaals1890()
        self.epsilonMixBehavior = epsilonMixvanderWaals1890()
