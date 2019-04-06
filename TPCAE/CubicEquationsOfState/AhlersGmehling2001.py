import numpy as np
from CubicEquationsOfState.PengAndRobinson1976 import PR1976, thetaiPR1976
from typing import List
from compounds import SubstanceProp
from constants import R_IG
from typing import List

from CubicEquationsOfState.PengAndRobinson1976 import PR1976, biPR1976, thetaiPR1976
from EOSParametersBehavior.ParametersBehaviorInterface import BiBehavior
from MixtureRules.ClassicMixtureRule import ClassicBMixture, ClassicMixtureRule
from MixtureRules.MixtureRulesInterface import (
    DeltaMixtureRuleBehavior,
    MixtureRuleBehavior,
    EpsilonMixtureRuleBehavior,
)
from compounds import SubstanceProp
from constants import R_IG


class ciAG2001(BiBehavior):
    def __init__(self):
        self.theta = thetaiPR1976()

    def getBi(self, i: int, T: float, substances: List[SubstanceProp]) -> float:
        return self.getCi(i, T, substances)

    def gamma(self, i: int, substances: List[SubstanceProp]) -> float:
        zc = substances[i].Zc
        return 12.67 + zc * (-107.21 + zc * 246.78)

    def eta(self, i: int, substances: List[SubstanceProp]) -> float:
        zc = substances[i].Zc
        return 26.966 - 74.458 * zc

    def beta(self, i: int, T: float, substances: List[SubstanceProp]) -> float:
        tr = T / substances[i].Tc
        gamma = self.gamma(i, substances)
        eta = self.eta(i, substances)
        alpha = self.theta.alpha(i, T, substances)
        return 0.35 / (0.35 + (eta * np.abs(tr - alpha)) ** gamma)

    def cc(self, i: int, substances: List[SubstanceProp]) -> float:
        zc = substances[i].Zc
        tc = substances[i].Tc
        pc = substances[i].Pc
        return (0.3074 - zc) * R_IG * tc / pc

    def getCi(self, i: int, T: float, substances: List[SubstanceProp]) -> float:
        return self.cc(i, substances) * self.beta(i, T, substances)


class cmAG2001:
    def __init__(self):
        self.cmBehavior = ClassicBMixture()
        self.ciBehavior = ciAG2001()

    def cm(self, y, T: float, substances) -> float:
        return self.cmBehavior.bm(y, T, self.ciBehavior, substances)

    def diffCm(self, i: int, y, T: float, substances) -> float:
        return self.ciBehavior.getBi(i, T, substances)


class BMixtureRuleBehaviorVolumeTranslated(ClassicBMixture):
    def __init__(self):
        self.cm = cmAG2001()

    def bm(self, y, T: float, bib: BiBehavior, substances) -> float:
        s1 = 0.0
        for i in range(len(y)):
            s1 += y[i] * bib.getBi(i, T, substances)
        return s1 - self.cm.cm(y, T, substances)

    def diffBm(self, i: int, y, T: float, bib: BiBehavior, substances) -> float:
        return bib.getBi(i, T, substances) - self.cm.ciBehavior.getCi(i, T, substances)


class ClassicMixtureRuleVolumeTranslated(ClassicMixtureRule):
    def __init__(self):
        super().__init__()
        self.bmBehavior = BMixtureRuleBehaviorVolumeTranslated()


class deltaMixAG2001(DeltaMixtureRuleBehavior):
    def __init__(self):
        self.cm = cmAG2001()

    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return 2.0 * bmb.bm(y, T, bib, substances) + 4.0 * self.cm.cm(y, T, substances)

    def diffDeltam(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return 2.0 * bmb.diffBm(i, y, T, bib, substances) + 4.0 * self.cm.diffCm(
            i, y, T, substances
        )


class epsilonMixAG2001(EpsilonMixtureRuleBehavior):
    def __init__(self):
        self.cm = cmAG2001()

    def epsilonm(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return (
            -(bmb.bm(y, T, bib, substances)) ** 2
            + 2.0 * (self.cm.cm(y, T, substances)) ** 2
        )

    def diffEpsilonm(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return -2.0 * bmb.bm(y, T, bib, substances) * bmb.diffBm(
            i, y, T, bib, substances
        ) + 4.0 * self.cm.cm(y, T, substances) * self.cm.diffCm(i, y, T, substances)


class AG2001(PR1976):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Ahlers-Gmehling (2001)"
        self.deltaMixBehavior = deltaMixAG2001()
        self.epsilonMixBehavior = epsilonMixAG2001()
        self.mixRuleBehavior = ClassicMixtureRuleVolumeTranslated()
