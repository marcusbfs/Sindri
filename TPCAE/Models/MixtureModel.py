from typing import List

import numpy as np

from EOSMixture import EOSMixture
from Factories.EOSMixFactory import createEOSMix
from Properties import Props
from compounds import SubstanceProp


class MixtureModel:
    def __init__(self):

        self.propsliq: Props = None
        self.propsvap: Props = None
        self.system: EOSMixture = None

        self.T: float = 150
        self.P: float = 1e5
        self.Tref: float = 300
        self.Pref: float = 150
        self.y: List[float] = []
        self.k: List[List[float]] = [[]]
        self.eosname: str = "Peng and Robinson (1974)"
        # VLE
        self.T_vle: float = 150
        self.P_vle: float = 1e5
        self.y_vle: List[float] = []
        self.binaryDiagram_type = "isothermal"  # or isobaric

        self.substances_in_the_system: List[SubstanceProp] = []
        self.EOSObservers = []
        self.RefObservers = []
        self.ProcObservers = []
        self.SubstanceObservers = []
        self.CalculationObservers = []
        self.info: str = ""
        self.log: str = ""

    # ================== SETTERS =========================

    def setProc(self, p: float, t: float):
        self.P = p
        self.T = t
        self.notifyProcObservers()

    def setRef(self, p: float, t: float):
        self.Pref = p
        self.Tref = t
        self.notifyRefObservers()

    def setEOS(self, s: str):
        self.eosname = s
        self.setupSystem()
        self.notifyEOSObservers()

    def addSubstanceToSystem(self, substance: SubstanceProp):
        self.substances_in_the_system.append(substance)
        self.updateK()
        self.setupSystem()
        self.notifySubstanceObservers()

    def clearSubstancesInSystem(self):
        self.substances_in_the_system: List[SubstanceProp] = []
        self.updateK()
        self.setupSystem()
        self.notifySubstanceObservers()

    def removeSubstanceFromSystem(self, substance: str):
        if self.getNumberOfSubstancesInSystem() > 0:
            for s in self.substances_in_the_system:
                if s.Name == substance:
                    self.substances_in_the_system.remove(s)
                    self.updateK()
                    self.setupSystem()
                    self.notifySubstanceObservers()
                    return

    def setMolarFractions(self, y: List[float]):
        if len(y) != self.getNumberOfSubstancesInSystem():
            raise ValueError(
                "Number of molar fractions not equals number of substances in the system"
            )
        if np.abs(np.sum(y) - 1.0) > 1e-10:
            raise ValueError("Molar fractions doesn't sum to one")
        self.y = y

    def setBinaryInteractionsParameters(self, k: List[List[float]]):
        self.k = k
        self.setupSystem()

    def setupSystem(self):
        self.system = createEOSMix(self.substances_in_the_system, self.eosname, self.k)

    def setVLEPT(self, p: float, t: float):
        self.P_vle, self.T_vle = p, t

    def setVLEMolarFractions(self, y: List[float]):
        if len(y) != self.getNumberOfSubstancesInSystem():
            raise ValueError(
                "Number of molar fractions not equals number of substances in the system"
            )
        if np.sum(y) != 1.0:
            raise ValueError("Molar fractions doesn't sum to one")
        self.y_vle = y

    def setBinaryDiagramType(self, t: str):
        self.binaryDiagram_type = t

    # ================== GETTERS =========================

    def getPref(self) -> float:
        return self.Pref

    def getP(self) -> float:
        return self.P

    def getTref(self) -> float:
        return self.Tref

    def getT(self) -> float:
        return self.T

    def getEOS(self) -> str:
        return self.eosname

    def getSubstancesInSystems(self) -> List[SubstanceProp]:
        return self.substances_in_the_system

    def getNumberOfSubstancesInSystem(self) -> int:
        return len(self.substances_in_the_system)

    def getMolarFractions(self) -> List[float]:
        return self.y

    def getBinaryInteractionsParameters(self) -> List[List[float]]:
        return self.k

    def isBinaryMixture(self) -> bool:
        return self.getNumberOfSubstancesInSystem() == 2

    def getPropsLiq(self) -> Props:
        return self.propsliq

    def getPropsVap(self) -> Props:
        return self.propsvap

    def getVLEMolarFractions(self) -> List[float]:
        return self.y_vle

    def getVLEMolarFractions(self) -> List[float]:
        return self.y_vle

    def getBinaryDiagramType(self) -> str:
        return self.binaryDiagram_type

    def updateK(self):
        n = self.getNumberOfSubstancesInSystem()
        self.k = np.zeros((n, n), dtype=np.float64)

    # ================= CALCULATIONS ==============

    def calculations(self):
        try:
            self.propsliq, self.propsvap = self.system.getAllProps(
                self.y, self.Tref, self.T, self.Pref, self.P
            )
            self.notifyCalculationsObserver()
        except Exception as e:
            raise ValueError(
                "Error calculating properties of mixture\n{}".format(str(e))
            )

    # Observers registers

    def registerEOSObserver(self, o):
        self.EOSObservers.append(o)

    def registerRefObserver(self, o):
        self.RefObservers.append(o)

    def registerProcObserver(self, o):
        self.ProcObservers.append(o)

    def registerSubstanceObserver(self, o):
        self.SubstanceObservers.append(o)

    def registerCalculationsObserver(self, o):
        self.CalculationObservers.append(o)

    # Observers notify
    def notifyEOSObservers(self):
        for o in self.EOSObservers:
            o.updateEOS()

    def notifyRefObservers(self):
        for o in self.RefObservers:
            o.updateRef()

    def notifyProcObservers(self):
        for o in self.ProcObservers:
            o.updateProc()

    def notifySubstanceObservers(self):
        for o in self.SubstanceObservers:
            o.updateSubstance()

    def notifyCalculationsObserver(self):
        for o in self.CalculationObservers:
            o.updateCalculations()


if __name__ == "__main__":

    m = MixtureModel()
    m.addSubstanceToSystem(SubstanceProp("methane", "CH4"))
    print(m.getEOS())
    print(m.getNumberOfSubstancesInSystem())
