from PySide2 import QtWidgets
from PySide2.QtWidgets import QMessageBox
import numpy as np
from typing import List

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
        self.report = None

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

    def saveToTxtClicked(self):
        if self.mixtureCalcView.plainTextEdit_information.toPlainText() == "":
            til = "No data"
            msg = "Please, generate the data first"
            QtWidgets.QMessageBox.about(self.mixtureCalcView, til, msg)
            return
        try:
            name_suggestion = "mixture01" + ".txt"
            txt_file_name = QtWidgets.QFileDialog.getSaveFileName(
                self.mixtureCalcView, "Save file", name_suggestion, "Text files (*.txt)"
            )[0]
            if not txt_file_name:
                return 0
            info = self.mixtureCalcView.plainTextEdit_information.toPlainText()
            log = self.mixtureCalcView.plainTextEdit_log.toPlainText()
            file_content = info + "\n\n" + self.report + "\n--- LOG ---\n" + log
            try:
                with open(txt_file_name, "w") as f:
                    f.write(file_content)
                til = "Successful"
                msg = "The data has been successfully saved."
            except Exception as e:
                til = "Problem"
                msg = "The data couldn't be saved.\n" + str(e)
            QtWidgets.QMessageBox.about(self.mixtureCalcView, til, msg)

        except Exception as e:
            if (
                str(e)
                == "'Window_PureSubstanceCalculations' object has no attribute 'report'"
            ):
                til = "Missing data"
                msg = "Please, generate the data first."
            else:
                til = "Error generating txt file"
                msg = str(e)
            QtWidgets.QMessageBox.about(self.mixtureCalcView, til, msg)
            return -1

    def setReport(self, s: str):
        self.report = s

    def saveSystemClicked(self):
        n = self.model.getNumberOfSubstancesInSystem()
        if n < 2:
            til = "No mixture"
            msg = "Please, select two or more substances"
            QtWidgets.QMessageBox.about(self.mixtureCalcView, til, msg)
            return

        import _devinfo

        try:
            _file_extension = _devinfo.__MIXTURESYSTEM_FILE_EXTENSION__
            name_suggestion = "mixture_system" + _file_extension
            txt_file_name = QtWidgets.QFileDialog.getSaveFileName(
                self.mixtureCalcView,
                "Save file",
                name_suggestion,
                "{} files (*{})".format(_devinfo.__SOFTWARE_NAME__, _file_extension),
            )[0]
            if not txt_file_name:
                return 0
            try:
                import datetime

                now = datetime.datetime.now()
                dateandtime = now.strftime("%H:%M %d-%m-%Y")

                file_content = ""
                # Header (two lines)
                file_content += _devinfo.__SOFTWARE_NAME__ + " MIXTURE SYSTEM\n"
                file_content += dateandtime + "\n"
                file_content += "\n"

                # number of components
                file_content += str(n) + "\n"
                file_content += "\n"

                y = self.getMolarFractionsFromTable(
                    self.mixtureCalcView.tableWidget_MixtureSystem, 2
                )
                k = self.model.getBinaryInteractionsParameters()

                # Name, formula and molar fraction
                for i in range(n):
                    name = self.mixtureCalcView.tableWidget_MixtureSystem.item(
                        i, 0
                    ).text()
                    formula = self.mixtureCalcView.tableWidget_MixtureSystem.item(
                        i, 1
                    ).text()
                    file_content += '"{0:s}"\t"{1:s}"\t{2:0.17f}\n'.format(
                        name, formula, y[i]
                    )

                file_content += "\n"

                # binary interaction parameters
                for i in range(n):
                    for j in range(n - 1):
                        file_content += "{0:0.17f}\t".format(k[i][j])
                    file_content += "{0:0.17f}\n".format(k[i][n - 1])

                with open(txt_file_name, "w") as f:
                    f.write(file_content)
                til = "Successful"
                msg = "The system has been successfully saved."
            except Exception as e:
                til = "Error"
                msg = "The system couldn't be saved.\n" + str(e)
            QtWidgets.QMessageBox.about(self.mixtureCalcView, til, msg)

        except Exception as e:
            til = "Error generating txt file"
            msg = str(e)
            QtWidgets.QMessageBox.about(self.mixtureCalcView, til, msg)
            return -1

    def loadSystemClicked(self):
        import _devinfo
        import shlex

        _file_extension = _devinfo.__MIXTURESYSTEM_FILE_EXTENSION__
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self.mixtureCalcView,
            "Load file",
            "",
            "{} files (*{})".format(_devinfo.__SOFTWARE_NAME__, _file_extension),
        )[0]

        if not filename:
            return 0

        try:
            with open(filename, "r") as file:
                skiplines = 3
                for i in range(skiplines):
                    file.readline()
                content = [line.rstrip("\n") for line in file if line != "\n"]

            n = int(content[0])
            y = np.empty(n, dtype=np.float64)
            k = np.empty([n, n], dtype=np.float64)
            self.mixtureCalcView.tableWidget_MixtureSystem.setRowCount(n)

            index = 1
            # substances : List[SubstanceProp] = []
            self.model.clearSubstancesInSystem()
            for i in range(n):
                subs = shlex.split(content[index + i])
                name = QtWidgets.QTableWidgetItem(subs[0])
                formula = QtWidgets.QTableWidgetItem(subs[1])
                molar_fraction = QtWidgets.QTableWidgetItem(subs[2])
                y[i] = float(subs[2])
                self.mixtureCalcView.tableWidget_MixtureSystem.setItem(i, 0, name)
                self.mixtureCalcView.tableWidget_MixtureSystem.setItem(i, 1, formula)
                self.mixtureCalcView.tableWidget_MixtureSystem.setItem(
                    i, 2, molar_fraction
                )
                self.model.addSubstanceToSystem(
                    SubstanceProp(name.text(), formula.text())
                )
                # substances.append(SubstanceProp(n, f))

            index += n
            for i in range(n):
                for j in range(n):
                    ks = shlex.split(content[index + i])
                    k[i][j] = float(ks[j])

            self.model.setBinaryInteractionsParameters(k)

        except Exception as e:
            title = "Error loading system"
            msg = 'Error reading from file "' + filename + '"\n' + str(e)
            QtWidgets.QMessageBox.about(self.mixtureCalcView, title, msg)

    def VLEClicked(self):
        n = self.model.getNumberOfSubstancesInSystem()
        if n < 2:
            QtWidgets.QMessageBox.about(
                self.mixtureCalcView, "Error", "Please, select two or more substances"
            )
            return
        from Controllers.MixtureVLEController import MixtureVLEController

        mixtureVLEController = MixtureVLEController(self, self.model)
        mixtureVLEController.createMixVLEView()
