from EOSPureSubstanceInterface import EOSPureSubstanceInterface
from Properties import VaporPressure
from compounds import FluidState
from compounds import SubstanceProp


class PureSubstanceModel:
    def __init__(self):
        self.T: float = 150
        self.P: float = 1e5
        self.Tref: float = 300
        self.Pref: float = 150
        self.substances_name: str
        self.eosname: str = "Peng and Robinson (1974)"
        self.system: EOSPureSubstanceInterface
        self.EOSObservers = []
        self.RefObservers = []
        self.ProcObservers = []
        self.SubstanceObservers = []
        self.CalculationObservers = []
        self.state = FluidState.Unknown
        self.log = ""

    def setupSystem(self):
        self.substance = SubstanceProp(self.substance_name, self.formula)
        # self.mix = MixtureProp([self.substance], [1.0])
        self.system = EOSPureSubstanceInterface([self.substance], self.eosname)
        self.log = ""

    def getZ(self):
        return self.system.getZfromPT(self.P, self.T)

    def getAllProps(self):
        return self.system.getAllProps(self.Tref, self.T, self.Pref, self.T)

    def setT(self, v: float):
        self.T = v
        self.notifyProcObservers()

    def setTref(self, v: float):
        self.Tref = v
        self.notifyRefObservers()

    def setP(self, v: float):
        self.P = v
        self.notifyProcObservers()

    def setPref(self, v: float):
        self.Pref = v
        self.notifyRefObservers()

    def getT(self) -> float:
        return self.T

    def getTref(self) -> float:
        return self.Tref

    def getP(self) -> float:
        return self.P

    def getPref(self) -> float:
        return self.Pref

    def setEOS(self, s: str):
        self.eosname = s
        self.notifyEOSObservers()

    def setSubstance(self, s: str, f: str):
        self.substance_name = s
        self.formula = f
        self.notifySubstanceObservers()

    def getEOS(self) -> str:
        return self.eosname

    def getSubstanceName(self) -> str:
        return self.substance_name

    def getSubstanceFormula(self) -> str:
        return self.formula

    def getSubstanceProps(self):
        self.substance.getFluidState(self.P, self.T, self.system)

    def getFluidState(self):
        return self.fluidState

    def getFluidStateFlag(self):
        return self.state

    def getLog(self):
        return self.log

    def getPvp(self):
        return self.Pvp

    def getPropsLiq(self):
        return self.propsliq

    def getPropsVap(self):
        return self.propsvap

    def calculate(self):
        try:
            self.fluidState = self.substance.getFluidState(self.P, self.T, self.system)
            self.state = self.substance.getFluidStateFlag()
        except:
            raise ValueError(
                "One or more of the following properties is not set: Tc, Pc, omega"
            )

        try:  # calculate properties at T and P

            self.propsliq, self.propsvap = self.system.getAllProps(
                self.Tref, self.T, self.Pref, self.P
            )

            # Not in supecritical or gaseous (T > Tc) state
            if self.substance.state not in (FluidState.Supercritical, FluidState.Gas):
                self.PvpAW = self.substance.getPvpAW(self.T)
                self.PvpLK = self.substance.getPvpLK(self.T)
                self.PvpAnt = self.substance.getPvpAntoine(self.T)
                self.AntLog = self.substance.getAntoineLog(self.T)
                self.PvpEOS, self.PvpEOS_iter = self.system.getPvp(self.T, self.PvpAW)

                self.Pvp = VaporPressure()
                self.Pvp.setEOS(self.PvpEOS)
                self.Pvp.setAW(self.PvpAW)
                self.Pvp.setLK(self.PvpLK)
                self.Pvp.setAntoine(self.PvpAnt)
                self.Pvp.AntonieLog = self.AntLog

                self.log = self.propsliq.log + self.AntLog

            # In supecritical or gaseous (T > Tc) state
            else:
                self.Pvp = None

        except Exception as e:
            raise ValueError(
                "Error calculating properties of single substance\n", str(e)
            )

        self.notifyCalculationsObserver()

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
