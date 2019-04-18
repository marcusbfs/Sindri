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

# TODO WHICH MIXTURE RULE FOR C?


def getZeta(i: int, substances):
    w = substances[i].omega
    return 0.3211 + w * (-0.08 + 0.0384 * w)


def getBeta(i: int, substances):
    zeta = getZeta(i, substances)
    return 0.1077 + zeta * (0.76405 + zeta * (-1.24282 + zeta * 0.9621))


class biHK1980(BiBehavior):
    def getBi(self, i: int, T: float, substances) -> float:
        return (
            getBeta(i, substances)
            * getZeta(i, substances)
            / (substances[i].Pc / (R_IG * substances[i].Tc))
        )


class thetaiHK1980(ThetaiBehavior):
    def a(self, i: int, T: float, substances):
        zeta = getZeta(i, substances)
        beta = getBeta(i, substances)
        omega_a = (
            1.0
            - 3.0 * zeta
            + 3.0 * zeta ** 2
            + beta * zeta * (3.0 - 6.0 * zeta + beta * zeta)
        )
        return omega_a * np.power(R_IG * substances[i].Tc, 2) / substances[i].Pc

    def m(self, i: int, T: float, substances):
        w = substances[i].omega
        return 0.37464 + 1.54226 * w - 0.26992 * w * w

    def alpha(self, i: int, T: float, substances):
        _m = self.m(i, T, substances)
        return np.power(1.0 + _m * (1.0 - np.sqrt(T / substances[i].Tc)), 2)

    def getThetai(self, i: int, T: float, substances) -> float:
        return self.alpha(i, T, substances) * self.a(i, T, substances)


class deltaMixHK1980(DeltaMixtureRuleBehavior):
    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return 2.0 * bmb.bm(y, T, bib, substances)

    def diffDeltam(
        self, i: int, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        return 2.0 * bmb.diffBm(i, y, T, bib, substances)


class epsilonMixHK1980(EpsilonMixtureRuleBehavior):
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


class HK1980(EOSMixture):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Harmens and Knapp (1980)"
        self.mixRuleBehavior = ClassicMixtureRule()
        self.biBehavior = biHK1980()
        self.thetaiBehavior = thetaiHK1980()
        self.deltaMixBehavior = deltaMixHK1980()
        self.epsilonMixBehavior = epsilonMixHK1980()
