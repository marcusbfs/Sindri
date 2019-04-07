import numpy as np

from CubicEquationsOfState.Wilson1964 import Wilson1964, thetaiWilson1964


class thetaiSoave1972(thetaiWilson1964):
    def m(self, i: int, T: float, substances):
        w = substances[i].omega
        return 0.48 + w * (1.574 - 0.176 * w)

    def alpha(self, i: int, T: float, substances):
        tr = T / substances[i].Tc
        m = self.m(i, T, substances)
        return (1.0 + m * (1.0 - np.sqrt(tr))) ** 2


class Soave1972(Wilson1964):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Soave (1972)"
        self.thetaiBehavior = thetaiSoave1972()
