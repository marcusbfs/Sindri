from __future__ import annotations

from constants import DBL_EPSILON


class DeltaProp(object):
    def __init__(self, cp: float, h: float, s: float, g: float, u: float, a: float):
        self.Cp = cp
        self.H = h
        self.S = s
        self.G = g
        self.U = u
        self.A = a

    def subtract(self, dp2: DeltaProp) -> DeltaProp:
        cp = self.Cp - dp2.Cp
        h = self.H - dp2.H
        s = self.S - dp2.S
        g = self.G - dp2.G
        u = self.U - dp2.U
        a = self.A - dp2.A
        return DeltaProp(cp, h, s, g, u, a)

    def isEqual(self, dp2: DeltaProp, tol=1e-5) -> bool:
        if (
            self._relAbsErr(self.Cp, dp2.Cp) < tol
            and self._relAbsErr(self.H, dp2.H) < tol
            and self._relAbsErr(self.S, dp2.S) < tol
            and self._relAbsErr(self.G, dp2.G) < tol
            and self._relAbsErr(self.U, dp2.U) < tol
            and self._relAbsErr(self.A, dp2.A) < tol
        ):
            return True
        return False

    def _relAbsErr(self, x: float, y: float) -> float:
        if abs(x) < DBL_EPSILON:
            return abs(x - y)
        return abs((x - y) / x)


class VaporPressure(object):
    """
    Class containing information about the vapor pressure of a single substance system.
    """

    def __init__(self):
        self.EOS = 0
        self.AW = 0
        self.LK = 0
        self.Antoine = 0
        self.AntonieLog = 0

    def setEOS(self, v: float):
        self.EOS = v

    def setAW(self, v: float):
        self.AW = v

    def setLK(self, v: float):
        self.LK = v

    def setAntoine(self, v: float, log=""):
        self.Antoine = v
        self.AntonieLog = log

    def getAWerr(self) -> float:
        return self._relError(self.EOS, self.AW)

    def getLKerr(self) -> float:
        return self._relError(self.EOS, self.LK)

    def getAntoineerr(self) -> float:
        return self._relError(self.EOS, self.Antoine)

    def _relError(self, _x: float, _y: float) -> float:
        if abs(_x) < DBL_EPSILON:
            return _x - _y
        return (_x - _y) / _x


class Props(object):
    def __init__(self):
        self.P = 0
        self.T = 0
        self.Z = 0
        self.V = 0
        self.rho = 0
        self.Pvp = 0
        self.Fugacity = 0
        self.Props = 0
        self.IGProps = 0
        self.log = ""

    def setRho(self, v: float):
        self.rho = v

    def setPvp(self, v: VaporPressure):
        self.Pvp = v

    def setProps(self, v: DeltaProp):
        self.Props = v

    def setIGProps(self, v: DeltaProp):
        self.IGProps = v

    def setIGProps(self, v: float):
        self.Fugacity = v
