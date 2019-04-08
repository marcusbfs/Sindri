from PySide2 import QtWidgets

from Models.PureSubstanceModel import PureSubstanceModel
from Views.PureSubstanceView import PureSubstanceView
from units import conv_unit


class PureSubstanceController:
    def __init__(self, model: PureSubstanceModel):
        self.model = model

        self.units = {
            "P": "bar",
            "T": "K",
            "V": "m3/mol",
            "rho": "kg/m3",
            "energy_per_mol": "J/mol",
            "energy_per_mol_temp": "J/molK",
        }

        self.view = PureSubstanceView(self, self.model)

        # self.model.registerEOSObserver(self)
        # self.model.registerSubstanceObserver(self)

    # getters

    def createView(self):
        self.view.show()

    def getZ(self):
        return self.model.getZ()

    # setters

    def setRef(self, p: float, t: float):
        self.model.setPref(p)
        self.model.setTref(t)

    def setProc(self, p: float, t: float):
        self.model.setP(p)
        self.model.setT(t)

    def setEOS(self, n: str):
        self.model.setEOS(n)

    def setSubstance(self, n: str, f: str):
        self.model.setSubstance(n, f)

    def updateEOS(self):
        print(id(self), "New EOS: {}".format(self.model.getEOS()))

    def calculate(self):

        self.procTunit = self.view.comboBox_procTunit.currentText()
        self.procPunit = self.view.comboBox_procPunit.currentText()
        self.refTunit = self.view.comboBox_refTunit.currentText()
        self.refPunit = self.view.comboBox_refPunit.currentText()

        try:
            self.T = conv_unit(
                float(self.view.le_procT.text()), self.procTunit, "K"
            )  # convert to Kelvin
            self.P = conv_unit(
                float(self.view.le_procP.text()), self.procPunit, "Pa"
            )  # convert to pascal
            self.Tref = conv_unit(
                float(self.view.le_refT.text()), self.refTunit, "K"
            )  # convert to Kelvin
            self.Pref = conv_unit(
                float(self.view.le_refP.text()), self.refPunit, "Pa"
            )  # convert to pascal
        except:
            # TODO
            print("error process variables")
            msg = QtWidgets.QMessageBox.about(
                self.view, "Error", "Invalid values for T and/or P"
            )
            return 1

        if (
            len(self.model.getSubstanceName().strip()) > 1
            and len(self.model.getEOS().strip()) > 1
        ):
            try:
                self.model.setPref(self.Pref)
                self.model.setTref(self.Tref)
                self.model.setT(self.T)
                self.model.setP(self.P)
                self.model.setupSystem()
                self.model.calculate()
            except Exception as e:
                QtWidgets.QMessageBox.about(self.view, "Error", str(e))
        else:
            msg = QtWidgets.QMessageBox.about(
                self.view, "Error", "Please, select compound and EOS"
            )
            return

    def updateSubstance(self):
        print(
            "New substance: {} ({})".format(
                self.model.getSubstanceName(), self.model.getSubstanceFormula()
            )
        )
