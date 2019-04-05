from typing import List

from CubicEquationsOfState.PengAndRobinson1976 import PR1976, biPR1976, thetaiPR1976
from EOSParametersBehavior.ParametersBehaviorInterface import BiBehavior
from MixtureRules.ClassicMixtureRule import ClassicBMixture
from MixtureRules.MixtureRulesInterface import (
    DeltaMixtureRuleBehavior,
    MixtureRuleBehavior,
    EpsilonMixtureRuleBehavior,
)
from compounds import SubstanceProp
from constants import R_IG


class tiTC1998(BiBehavior):
    def getBi(self, i: int, T: float, substances: List[SubstanceProp]) -> float:
        return self.getTi(i, T, substances)

    def getTi(self, i: int, T: float, substances: List[SubstanceProp]) -> float:
        k1 = self.getk1(i, T, substances)
        k3 = self.getk3(i, substances)
        k2 = self.getk2(k3)
        tc = substances[i].Tc
        pc = substances[i].Pc
        one_minus_tr_pow_two_thirds = 1.0 - (T / tc) ** (2.0 / 3.0)
        return (R_IG * tc / pc) * (
            k1
            + k2 * one_minus_tr_pow_two_thirds
            + k3 * one_minus_tr_pow_two_thirds ** 2
        )

    def getk1(self, i: int, T: float, substances: List[SubstanceProp]) -> float:
        w = substances[i].omega
        return 0.00185 + w * (0.00438 + w * (0.36322 + w * (-0.90831 + w * 0.55885)))

    def getk2(selfs, k3: float):
        return -0.00542 + k3 * (
            -0.51112 + k3 * (0.04533 + k3 * (0.07447 - k3 * 0.03831))
        )

    def getk3(self, i: int, substances: List[SubstanceProp]):
        k = 0
        name = substances[i].Name
        if name == "water":
            k = 0.01471
        elif name == "methanol":
            k = -0.04426
        return k


class tmTC1998:
    def __init__(self):
        self.tmBehavior = ClassicBMixture()
        self.tiBehavior = tiTC1998()

    def tm(self, y, T: float, substances) -> float:
        return self.tmBehavior.bm(y, T, self.tiBehavior, substances)

    def diffTm(self, i: int, y, T: float, substances) -> float:
        return self.tiBehavior.getBi(i, T, substances)


class thetaiTC1998(thetaiPR1976):
    def alpha(self, i: int, T: float, substances: List[SubstanceProp]):
        tr = T / substances[i].Tc
        M = self.getM(i, substances)
        N = self.getN(i, substances)
        return (1.0 + M * (1.0 - tr) + N * (1.0 - tr) * (0.7 - tr)) ** 2

    def getM(self, i: int, substances: List[SubstanceProp]):
        w = substances[i].omega
        return 0.20473 + w * (0.83548 + w * (-0.1847 + w * (0.16675 - 0.09881 * w)))

    def getN(self, i: int, substances: List[SubstanceProp]):
        name = substances[i].Name
        N = 0
        if name == "water":
            N = 0.11560
        elif name == "methanol":
            N = 0.03221

        return N


class deltaMixTC1998(DeltaMixtureRuleBehavior):
    def __init__(self):
        self.tm = tmTC1998()

    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return 2.0 * bmb.bm(y, T, bib, substances) + 4.0 * self.tm.tm(y, T, substances)

    def diffDeltam(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return 2.0 * bmb.diffBm(i, y, T, bib, substances) + 4.0 * self.tm.diffTm(
            i, y, T, substances
        )


class epsilonMixTC1998(EpsilonMixtureRuleBehavior):
    def __init__(self):
        self.tm = tmTC1998()

    def epsilonm(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return (
            -(bmb.bm(y, T, bib, substances)) ** 2
            + 2.0 * (self.tm.tm(y, T, substances)) ** 2
        )

    def diffEpsilonm(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return -2.0 * bmb.bm(y, T, bib, substances) * bmb.diffBm(
            i, y, T, bib, substances
        ) + 4.0 * self.tm.tm(y, T, substances) * self.tm.diffTm(i, y, T, substances)


class biTC1998(BiBehavior):
    def __init__(self):
        self.prbi = biPR1976()
        self.TCti = tiTC1998()

    def getBi(self, i: int, T: float, substances: List[SubstanceProp]) -> float:
        return self.prbi.getBi(i, T, substances) - self.TCti.getBi(i, T, substances)


class TsaiChen1998(PR1976):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Tsai and Chen (1998)"
        self.thetaiBehavior = thetaiTC1998()
        self.deltaMixBehavior = deltaMixTC1998()
        self.epsilonMixBehavior = epsilonMixTC1998()
        self.biBehavior = biTC1998()
