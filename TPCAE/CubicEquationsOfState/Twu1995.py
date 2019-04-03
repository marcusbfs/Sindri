from CubicEquationsOfState.PengAndRobinson1976 import PR1976, thetaiPR1976
import numpy as np


class thetaiTwu1995(thetaiPR1976):
    def alpha(self, i: int, T: float, substances):
        tr = T / substances[i].Tc
        w = substances[i].omega
        alpha0 = (tr) ** (-0.171813) * 2.718281828459045235360 ** (
            0.125283 * (1 - (tr) ** 1.77634)
        )
        alpha1 = (tr) ** (-0.607352) * 2.718281828459045235360 ** (
            0.511614 * (1 - (tr) ** 2.20517)
        )
        alpha = alpha0 + w * (alpha1 - alpha0)
        return alpha


class Twu1995(PR1976):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Twu, et al. (1995)"
        self.thetaiBehavior = thetaiTwu1995()
