from CubicEquationsOfState.PengAndRobinson1976 import PR1976, thetaiPR1976
import numpy as np


class thetaiGasemTwuMod2001(thetaiPR1976):
    def alpha(self, i: int, T: float, substances):
        tr = T / substances[i].Tc
        w = substances[i].omega
        alpha0 = (tr) ** (-0.207176) * 2.718281828459045235360 ** (
            0.092099 * (1 - (tr) ** (1.94800))
        )
        alpha1 = (tr) ** (-0.502297) * 2.718281828459045235360 ** (
            0.603486 * (1 - (tr) ** (2.09626))
        )
        alpha = alpha0 + w * (alpha1 - alpha0)
        return alpha


class GasemTwuMod2001(PR1976):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Gasem, et al. Twu modification (2001)"
        self.thetaiBehavior = thetaiGasemTwuMod2001()
