import numpy as np

from EOSMixture import EOSMixture
from MixtureRules.ClassicMixtureRule import ClassicMixtureRule, ClassicBMixture
from MixtureRules.MixtureRulesInterface import (
    BiBehavior,
    ThetaiBehavior,
    DeltaMixtureRuleBehavior,
    EpsilonMixtureRuleBehavior,
    MixtureRuleBehavior,
)
from constants import R_IG


class biAdachi1985(BiBehavior):
    def getBi(self, i: int, T: float, substances) -> float:
        w = substances[i].omega
        omega_b = 0.08779 + w * (-0.02181 + w * (-0.06708 + 0.10617 * w))
        return omega_b / (substances[i].Pc / (R_IG * substances[i].Tc))


class thetaiAdachi1985(ThetaiBehavior):
    def a(self, i: int, T: float, substances):
        w = substances[i].omega
        omega_ac = 0.43711 + w * (0.02366 + w * (0.10538 + w * 0.10164))
        return omega_ac * np.power(R_IG * substances[i].Tc, 2) / substances[i].Pc

    def m(self, i: int, T: float, substances):
        w = substances[i].omega
        return 0.44060 + w * (1.7039 + w * (-1.728 + w * 0.9929))

    def alpha(self, i: int, T: float, substances):
        _m = self.m(i, T, substances)
        return np.power(1.0 + _m * (1.0 - np.sqrt(T / substances[i].Tc)), 2)

    def getThetai(self, i: int, T: float, substances) -> float:
        return self.alpha(i, T, substances) * self.a(i, T, substances)


class ciAdachi1985(BiBehavior):
    def getBi(self, i: int, T: float, substances) -> float:
        w = substances[i].omega
        omega_c = 0.0506 + w * (0.04184 + w * (0.16413 - w * 0.03975))
        return omega_c / (substances[i].Pc / (R_IG * substances[i].Tc))


class cmAdachi1985:
    def __init__(self):
        self.cmBehavior = ClassicBMixture()
        self.ciBehavior = ciAdachi1985()

    def cm(self, y, T: float, substances) -> float:
        return self.cmBehavior.bm(y, T, self.ciBehavior, substances)

    def diffCm(self, i: int, y, T: float, substances) -> float:
        return self.ciBehavior.getBi(i, T, substances)


class deltaMixAdachi1985(DeltaMixtureRuleBehavior):
    def __init__(self):
        self.cm = cmAdachi1985()

    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return 2.0 * self.cm.cm(y, T, substances)

    def diffDeltam(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return 2.0 * self.cm.diffCm(i, y, T, substances)


class epsilonMixAdachi1985(EpsilonMixtureRuleBehavior):
    def __init__(self):
        self.cm = cmAdachi1985()

    def epsilonm(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return -(self.cm.cm(y, T, substances)) ** 2

    def diffEpsilonm(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return -2.0 * self.cm.cm(y, T, substances) * self.cm.diffCm(i, y, T, substances)


class Adachi1985(EOSMixture):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Adachi, et al. (1985)"
        self.mixRuleBehavior = ClassicMixtureRule()
        self.biBehavior = biAdachi1985()
        self.thetaiBehavior = thetaiAdachi1985()
        self.deltaMixBehavior = deltaMixAdachi1985()
        self.epsilonMixBehavior = epsilonMixAdachi1985()
