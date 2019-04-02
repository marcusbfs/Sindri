import abc
import compounds
from EOSParametersBehavior.ParametersBehaviorInterface import (
    BiBehavior,
    DeltaiBehavior,
    ThetaiBehavior,
    EpsiloniBehavior,
)
import numpy as np
from MixtureRules.MixtureRulesInterface import (
    ThetaMixtureRuleBehavior,
    BMixtureRuleBehavior,
    DeltaMixtureRuleBehavior,
    EpsilonMixtureRuleBehavior,
    MixtureRuleBehavior,
)


class ClassicThetaMixture(ThetaMixtureRuleBehavior):
    def thetam(self, y, T: float, thetaib, substances, k) -> float:
        s1 = 0.0
        n = len(y)
        for i in range(n):
            s2 = 0.0
            thetai = thetaib.getThetai(i, T, substances)
            for j in range(n):
                thetaj = thetaib.getThetai(j, T, substances)
                s2 += y[i] * y[j] * np.sqrt(thetai * thetaj) * (1.0 - k[i][j])
            s1 += s2
        return s1

    def diffThetam(
        self, i: int, y, T: float, thetaib: ThetaiBehavior, substances, k
    ) -> float:
        s = 0.0
        n = len(y)
        for j in range(n):
            if j != i:
                alphai = np.sqrt(
                    thetaib.getThetai(i, T, substances)
                    * thetaib.getThetai(j, T, substances)
                ) * (1.0 - k[i][j])
                alphaj = np.sqrt(
                    thetaib.getThetai(i, T, substances)
                    * thetaib.getThetai(j, T, substances)
                ) * (1.0 - k[j][i])
                s += y[j] * (alphai + alphaj)
        return s + 2.0 * y[i] * thetaib.getThetai(i, T, substances)


class ClassicBMixture(BMixtureRuleBehavior):
    def bm(self, y, T: float, bib: BiBehavior, substances) -> float:
        s1 = 0.0
        for i in range(len(y)):
            s1 += y[i] * bib.getBi(i, T, substances)
        return s1

    def diffBm(self, i: int, y, T: float, bib: BiBehavior, substances) -> float:
        return bib.getBi(i, T, substances)


class ClassicMixtureRule(MixtureRuleBehavior):
    def __init__(self):
        self.bmBehavior = ClassicBMixture()
        self.thetamBehavior = ClassicThetaMixture()

    def bm(self, y, T: float, bib: BiBehavior, substances) -> float:
        return self.bmBehavior.bm(y, T, bib, substances)

    def diffBm(self, i: int, y, T: float, bib: BiBehavior, substances) -> float:
        return self.bmBehavior.diffBm(i, y, T, bib, substances)

    def thetam(self, y, T: float, thetaib: ThetaiBehavior, substances, k) -> float:
        return self.thetamBehavior.thetam(y, T, thetaib, substances, k)

    def diffThetam(
        self, i: int, y, T: float, thetaib: ThetaiBehavior, substances, k
    ) -> float:
        return self.thetamBehavior.diffThetam(i, y, T, thetaib, substances, k)
