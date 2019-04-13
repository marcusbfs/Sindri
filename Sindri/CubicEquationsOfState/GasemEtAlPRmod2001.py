from CubicEquationsOfState.PengAndRobinson1976 import PR1976, thetaiPR1976


class thetaiGasemPRmod2001(thetaiPR1976):
    def m(self, i: int, T: float, substances):
        w = substances[i].omega
        return 0.386590 + 1.50226 * w - 0.16870 * w * w


class GasemPRmod2001(PR1976):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Gasem, et al. PR modification (2001)"
        self.thetaiBehavior = thetaiGasemPRmod2001()
