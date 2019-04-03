from CubicEquationsOfState.Soave1972 import Soave1972, thetaiSoave1972
from constants import R_IG
from MixtureRules.MixtureRulesInterface import (
    BiBehavior,
    EpsiloniBehavior,
    EpsilonMixtureRuleBehavior,
    BMixtureRuleBehavior,
)


class thetaiSoave1984(thetaiSoave1972):

    def a(self, i: int, T: float, substances):
        return 0.42188 * (R_IG * substances[i].Tc) ** 2 / substances[i].Pc

    def m(self, i: int, T: float, substances):
        w = substances[i].omega
        #return 0.4998 + w* 1.5928 -w*w*0.19563 +  0.025*w*w*w
        return 0.4998 + w * (1.5928 + w * ( -0.19563 + 0.025 * w))


class biSoave1984(BiBehavior):
    def getBi(self, i: int, T: float, substances) -> float:
        return 0.08333 / (substances[i].Pc / (R_IG * substances[i].Tc))


class epsiloniSoave1984(EpsiloniBehavior):
    def getEpsiloni(self, b: float) -> float:
        return .001736*(b/.08333)**2

class epsilonMixSoave1984(EpsilonMixtureRuleBehavior):
    def epsilonm(
            self, y, T: float, bib: BiBehavior, bmb: BMixtureRuleBehavior, substances
    ) -> float:
        return .001736*(bmb.bm(y, T, bib, substances) /.08333)**2

    def diffEpsilonm(
            self,
            i: int,
            y,
            T: float,
            bib: BiBehavior,
            bmb: BMixtureRuleBehavior,
            substances,
    ) -> float:
        return (2.*.001736/.08333**2)*bmb.bm(y, T,bib, substances)*bmb.diffBm(i, y, T, bib, substances)


class Soave1984(Soave1972):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Soave (1984)"
        self.thetaiBehavior = thetaiSoave1984()
        self.biBehavior = biSoave1984()
        self.epsiloniBehavior = epsiloniSoave1984()
        self.epsilonMixBehavior = epsilonMixSoave1984()
