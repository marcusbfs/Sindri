from PySide2 import QtWidgets
from PySide2.QtWidgets import QMessageBox
import numpy as np

from Views.MixtureCalculationsView import MixtureCalculationsView
from Models.MixtureModel import MixtureModel
from Controllers.UnitsOptionsController import UnitsOptionsController
from Controllers.EditBinaryInteractionParametersController import (
    EditBinaryInteractionParametersController,
)
from compounds import SubstanceProp
from units import conv_unit
import units
import utils


class MixtureCalculationsController:
    def __init__(self, model: MixtureModel):

        self.units = {
            "P": "bar",
            "T": "K",
            "V": "m3/mol",
            "rho": "kg/m3",
            "energy_per_mol": "J/mol",
            "energy_per_mol_temp": "J/molK",
        }

        self.model = model

        self.mixtureCalcView: MixtureCalculationsView = MixtureCalculationsView(
            self, self.model
        )

        self.editBinIntController = EditBinaryInteractionParametersController(
            self.model
        )
        self.editBinIntController.registerBinInteractionObserver(self)

        self.unitsOptionsController = UnitsOptionsController()
        self.unitsOptionsController.registerUnitsOptionsObserver(self)

        self.mixtureCalcView.listWidget_eos_options.setCurrentRow(0)
        self.mixtureCalcView.tableWidget_searchSubstance.setCurrentCell(0, 0)

    def createMixtureCalcView(self):
        self.mixtureCalcView.show()

    def openUnitsOptionsClicked(self):
        self.unitsOptionsController.createUnitsOptionsView()

    def updateUnitsOptions(self):
        self.units = self.unitsOptionsController.units
        self.mixtureCalcView.units = self.units

    def addClicked(self):
        current_row = self.mixtureCalcView.tableWidget_searchSubstance.currentRow()
        if current_row > -1:
            name = self.mixtureCalcView.tableWidget_searchSubstance.item(current_row, 1)
            formula = self.mixtureCalcView.tableWidget_searchSubstance.item(
                current_row, 0
            )

            self.model.addSubstanceToSystem(SubstanceProp(name.text(), formula.text()))

            rowpos = self.mixtureCalcView.tableWidget_MixtureSystem.rowCount()
            self.mixtureCalcView.tableWidget_MixtureSystem.insertRow(rowpos)
            self.mixtureCalcView.tableWidget_MixtureSystem.setItem(
                rowpos, 0, QtWidgets.QTableWidgetItem(name)
            )
            self.mixtureCalcView.tableWidget_MixtureSystem.setItem(
                rowpos, 1, QtWidgets.QTableWidgetItem(formula)
            )
            self.mixtureCalcView.tableWidget_MixtureSystem.setItem(
                rowpos, 2, QtWidgets.QTableWidgetItem("0.0")
            )

    def removeClicked(self):

        current_row = self.mixtureCalcView.tableWidget_MixtureSystem.currentRow()
        if current_row > -1:
            sname = self.mixtureCalcView.tableWidget_MixtureSystem.item(
                current_row, 0
            ).text()
            self.model.removeSubstanceFromSystem(sname)
            self.mixtureCalcView.tableWidget_MixtureSystem.removeRow(current_row)

    def editBinIntClicked(self):
        self.editBinIntController.createBinInteractionView()

    def calculatePropsClicked(self):
        # validate system

        if self.model.getNumberOfSubstancesInSystem() < 2:
            QMessageBox.about(
                self.mixtureCalcView,
                "No mixture",
                "Please, select two or more substances",
            )
            return

        try:
            y = self.getMolarFractionsFromTable(
                self.mixtureCalcView.tableWidget_MixtureSystem, 2
            )
        except:
            QMessageBox.about(
                self.mixtureCalcView, "Error", "Invalid molar fraction numbers"
            )
            return -1
        if np.abs(np.sum(y) - 1.0) > 1e-10:
            QMessageBox.about(
                self.mixtureCalcView,
                "Invalid molar fractions",
                "Molar fractions doesn't sum up to one",
            )
            return

        try:
            procTunit = self.mixtureCalcView.comboBox_procTunit.currentText()
            procPunit = self.mixtureCalcView.comboBox_procPunit.currentText()
            refTunit = self.mixtureCalcView.comboBox_refTunit.currentText()
            refPunit = self.mixtureCalcView.comboBox_refPunit.currentText()
            self.T = conv_unit(
                float(self.mixtureCalcView.le_procT.text()), procTunit, "K"
            )  # convert to Kelvin
            self.P = conv_unit(
                float(self.mixtureCalcView.le_procP.text()), procPunit, "Pa"
            )  # convert to pascal
            self.Tref = conv_unit(
                float(self.mixtureCalcView.le_refT.text()), refTunit, "K"
            )  # convert to Kelvin
            self.Pref = conv_unit(
                float(self.mixtureCalcView.le_refP.text()), refPunit, "Pa"
            )  # convert to pascal
        except:
            print("error process variables")
            msg = QtWidgets.QMessageBox.about(
                self.mixtureCalcView, "Error", "Process variables are not numbers"
            )
            return 1

        try:
            eosname = self.mixtureCalcView.listWidget_eos_options.currentItem().text()
            self.model.setMolarFractions(y)
            self.model.setEOS(eosname)
        except Exception as e:
            raise ValueError("Error in model setup\n", str(e))

        self.mixtureCalcView.plainTextEdit_information.clear()
        self.mixtureCalcView.tableWidget_results.setRowCount(0)
        self.mixtureCalcView.plainTextEdit_log.clear()

        try:
            # self.eoseq = EOS(self.mix, self.k, self.eosname)

            self.info = ""
            tab = "    "
            self.info += "Mixture:\n"

            for i in range(self.model.getNumberOfSubstancesInSystem()):
                n = self.model.getSubstancesInSystems()[i].Name
                f = self.model.getSubstancesInSystems()[i].Formula
                z = self.model.getMolarFractions()[i]
                self.info += tab + "{:} ({:}) [{:0.4f}]\n".format(n, f, z)

            self.info += "Equation of state: {0:s}\n".format(self.model.getEOS())
            self.info += "Process state: {0:.3f} {1:s}, {2:s} {3:s}\n".format(
                conv_unit(self.model.getT(), "K", self.units["T"]),
                self.units["T"],
                utils.f2str(
                    conv_unit(self.model.getP(), "Pa", self.units["P"]),
                    3,
                    lt=1e-2,
                    gt=1e4,
                ),
                self.units["P"],
            )
            self.info += "Reference state: {0:.3f} {1:s}, {2:s} {3:s}\n".format(
                conv_unit(self.model.getTref(), "K", self.units["T"]),
                self.units["T"],
                utils.f2str(
                    conv_unit(self.model.getPref(), "Pa", self.units["P"]),
                    3,
                    lt=1e-2,
                    gt=1e4,
                ),
                self.units["P"],
            )
            self.mixtureCalcView.plainTextEdit_information.appendPlainText(self.info)
        except Exception as e:
            print(e)
            err = "One or more of the following properties is not set: Tc, Pc, omega"
            msg = QtWidgets.QMessageBox.about(
                self.mixtureCalcView, "Properties error", str(err)
            )
            return 1

        try:
            self.model.calculations()
        except Exception as e:
            raise ValueError("Error calculating properties\n", str(e))

    def getMolarFractionsFromTable(self, table, col: int):
        n = self.model.getNumberOfSubstancesInSystem()
        y = np.empty(n, dtype=np.float64)
        for i in range(n):
            tmpn = table.item(i, col).text()
            try:
                tmpn = float(tmpn)
                t = tmpn * 1.0 + 1.0
                y[i] = tmpn
            except Exception as e:
                raise ValueError("Molar fractions are not valid numbers\n", str(e))
        return y

    def updateBinInteraction(self):
        self.model.setBinaryInteractionsParameters(self.editBinIntController.getK())

    def setEquimolarClicked(self):
        n = self.model.getNumberOfSubstancesInSystem()
        for i in range(n):
            self.mixtureCalcView.tableWidget_MixtureSystem.setItem(
                i, 2, QtWidgets.QTableWidgetItem(str(1.0 / n))
            )
