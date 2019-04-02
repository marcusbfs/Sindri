import abc
import compounds
from polyEqSolver import solve_cubic
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
from constants import R_IG


class EOSMixture:
    def __init__(self, _subs, _k):
        self.substances = _subs
        self.k = _k
        self.eosname = ""
        self.mixRuleBehavior = MixtureRuleBehavior()
        self.thetaiBehavior = ThetaiBehavior()
        self.biBehavior = BiBehavior()
        self.deltaiBehavior = DeltaiBehavior()
        self.epsiloniBehavior = EpsiloniBehavior()
        self.deltaMixBehavior = DeltaMixtureRuleBehavior()
        self.epsilonMixBehavior = EpsilonMixtureRuleBehavior()

    def getZfromPT(self, P: float, T: float, y):

        b = self.mixRuleBehavior.bm(y, T, self.biBehavior, self.substances)
        theta = self.mixRuleBehavior.thetam(
            y, T, self.thetaiBehavior, self.substances, self.k
        )
        delta = self.deltaiBehavior.getDeltai(b)
        epsilon = self.epsiloniBehavior.getEpsiloni(b)

        Bl = b * P / (R_IG * T)
        deltal = delta * P / (R_IG * T)
        epsilonl = epsilon * np.power(P / (R_IG * T), 2)
        thetal = theta * P / np.power(R_IG * T, 2)

        # 0 = ax ^ 3 + b * x ^ 2 + c * x + d
        _a = 1.0
        _b = deltal - Bl - 1.0
        _c = thetal + epsilonl - deltal * (1.0 + Bl)
        _d = -(epsilonl * (Bl + 1.0) + Bl * thetal)

        roots = np.asarray(solve_cubic(_a, _b, _c, _d))
        real_values = roots[roots > 0]
        return real_values

    def getPhi_i(self, i: int, y, P: float, T: float, Z: float):

        RT = R_IG * T

        V = RT * Z / P

        bm = self.mixRuleBehavior.bm(y, T, self.biBehavior, self.substances)

        thetam = self.mixRuleBehavior.thetam(
            y, T, self.thetaiBehavior, self.substances, self.k
        )

        deltam = self.deltaiBehavior.getDeltai(bm)

        epsilonm = self.epsiloniBehavior.getEpsiloni(bm)

        deltam2_minus_4epislonm = deltam * deltam - 4.0 * epsilonm
        sqrt_d2_minus_4eps = np.sqrt(deltam2_minus_4epislonm)
        twoV_plus_deltam_minus_sqrtd24eps = 2.0 * V + deltam - sqrt_d2_minus_4eps
        twoV_plus_deltam_plus_sqrtd24eps = 2.0 * V + deltam + sqrt_d2_minus_4eps

        # derivatives
        diffthetam = self.mixRuleBehavior.diffThetam(
            i, y, T, self.thetaiBehavior, self.substances, self.k
        )
        diffbm = self.mixRuleBehavior.diffBm(i, y, T, self.biBehavior, self.substances)
        diffdeltam = self.deltaMixBehavior.diffDeltam(
            i, y, T, self.biBehavior, self.mixRuleBehavior, self.substances
        )
        diffepsilonm = self.epsilonMixBehavior.diffEpsilonm(
            i, y, T, self.biBehavior, self.mixRuleBehavior, self.substances
        )
        deltaN = deltam * diffdeltam * 2.0 - 4.0 * diffepsilonm

        # Equation(Poling, 2001)

        firstline = (1.0 / sqrt_d2_minus_4eps) * (diffthetam / RT) - (
            thetam / RT
        ) * deltaN / (2.0 * np.power(deltam2_minus_4epislonm, 1.5))

        secline_p1 = np.log(
            twoV_plus_deltam_minus_sqrtd24eps / twoV_plus_deltam_plus_sqrtd24eps
        )

        secline_p2 = (thetam / RT) / sqrt_d2_minus_4eps

        thirdline = (
            (diffdeltam - deltaN / (2.0 * sqrt_d2_minus_4eps))
            / twoV_plus_deltam_minus_sqrtd24eps
            - (diffdeltam + deltaN / (2.0 * sqrt_d2_minus_4eps))
            / twoV_plus_deltam_plus_sqrtd24eps
        )

        fourthline = diffbm / (V - bm) - np.log((V - bm) / V) - np.log(Z)

        lnphi_i = firstline * secline_p1 + secline_p2 * thirdline + fourthline
        phi_i = np.exp(lnphi_i)
        return phi_i