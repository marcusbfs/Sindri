from CubicEquationsOfState.PengAndRobinson1976 import PR1976, thetaiPR1976
import numpy as np


class thetaiGasem2001(thetaiPR1976):
    def alpha(self, i: int, T: float, substances):
        tr = T / substances[i].Tc
        w = substances[i].omega
        A = 2.0
        B = 0.836
        C = 0.134
        D = 0.508
        E = -0.0467
        return np.exp((A + B * tr) * (1.0 - tr ** (C + D * w + E * w * w)))


class Gasem2001(PR1976):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Gasem, et al. (2001)"
        self.thetaiBehavior = thetaiGasem2001()
