from CubicEquationsOfState.PengAndRobinson1976 import PR1976, thetaiPR1976


class thetaiSV1986(thetaiPR1976):
    def m(self, i: int, T: float, substances):
        w = substances[i].omega
        name = substances[i].Name
        k0 = 0.378893 + 1.48971530 * w - 0.17131848 * w ** 2 + 0.0196554 * w ** 3
        k1 = 0

        if name == "hexadecane":
            k1 = 0.02665
        elif name == "hexane":
            k1 = 0.05104
        elif name == "cyclohexane":
            k1 = 0.07023
        elif name == "methane":
            k1 = -0.00159
        elif name == "benzene":
            k1 = 0.07019

        Tr = T / substances[i].Tc
        k = k0 + k1 * (1 + Tr) * (0.7 - Tr)
        return k


class SV1986(PR1976):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Stryjek and Vera (1986)"
        self.thetaiBehavior = thetaiSV1986()
