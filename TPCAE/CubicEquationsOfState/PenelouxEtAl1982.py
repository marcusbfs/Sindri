from CubicEquationsOfState.Soave1972 import Soave1972
from CubicEquationsOfState.Wilson1964 import biWilson1964
from MixtureRules.MixtureRulesInterface import (
    BMixtureRuleBehavior,
    BiBehavior,
    DeltaiBehavior,
    DeltaMixtureRuleBehavior,
    EpsilonMixtureRuleBehavior,
    EpsiloniBehavior,
    MixtureRuleBehavior,
)
from MixtureRules.ClassicMixtureRule import ClassicMixtureRule, ClassicBMixture
from constants import R_IG


class CiBehavior:
    def getCi(self, i: int, T: float, substances):
        w = substances[i].omega
        return (
            0.40768
            * (R_IG * substances[i].Tc / substances[i].Pc)
            * (0.00385 + 0.08775 * w)
        )


class CMixBehavior:
    def __init__(self):
        self.ci = CiBehavior()

    def cm(self, y, T: float, substances):
        s = 0.0
        for i in range(len(y)):
            s += y[i] * self.ci.getCi(i, T, substances)
        return s


class BMixtureRuleBehaviorVolumeTranslated(ClassicBMixture):
    def __init__(self):
        self.cm = CMixBehavior()

    def bm(self, y, T: float, bib: BiBehavior, substances) -> float:
        s1 = 0.0
        for i in range(len(y)):
            s1 += y[i] * bib.getBi(i, T, substances)
        return s1 - self.cm.cm(y, T, substances)

    def diffBm(self, i: int, y, T: float, bib: BiBehavior, substances) -> float:
        return bib.getBi(i, T, substances) - self.cm.ci.getCi(i, T, substances)


class ClassicMixtureRuleVolumeTranslated(ClassicMixtureRule):
    def __init__(self):
        super().__init__()
        self.bmBehavior = BMixtureRuleBehaviorVolumeTranslated()


class deltaMixPeneloux1982(DeltaMixtureRuleBehavior):
    def __init__(self):
        self.cm = CMixBehavior()

    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        b = bmb.bm(y, T, bib, substances)
        c = self.cm.cm(y, T, substances)
        return b + 3.0 * c

    def diffDeltam(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return (
            bmb.diffBm(i, y, T, bib, substances)
            + self.cm.ci.getCi(i, T, substances) * 3.0
        )


class epsilonMixPeneloux1982(EpsilonMixtureRuleBehavior):
    def __init__(self):
        self.cm = CMixBehavior()

    def epsilonm(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        b = bmb.bm(y, T, bib, substances)
        c = self.cm.cm(y, T, substances)
        return b * c + 2.0 * c * c

    def diffEpsilonm(
        self,
        i: int,
        y,
        T: float,
        bib: BiBehavior,
        bmb: BMixtureRuleBehavior,
        substances,
    ) -> float:
        b = bmb.bm(y, T, bib, substances)
        bline = bmb.diffBm(i, y, T, bib, substances)
        c = self.cm.cm(y, T, substances)
        cline = self.cm.ci.getCi(i, T, substances)
        return bline * c + cline * b + 4.0 * c * cline


class PenelouxEtAl1982(Soave1972):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Peneloux et. al (1982)"
        self.mixRuleBehavior = ClassicMixtureRuleVolumeTranslated()
        self.deltaMixBehavior = deltaMixPeneloux1982()
        self.epsilonMixBehavior = epsilonMixPeneloux1982()
