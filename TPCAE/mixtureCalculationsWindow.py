import os

import numpy as np
from PySide2 import QtCore, QtWidgets

import db
import db_utils
import eos
import reports
import units
import utils
from Properties import VaporPressure
from VLEWindow import Window_VLE
from compounds import MixtureProp, SubstanceProp
from editBinaryInteractionsParametersWin import Window_BinaryInteractionParameters
from eos import EOS
from ui.mixture_calculations_ui import Ui_MixtureCalculationWindow
from units import conv_unit
from unitsOptionsWindow import Window_UnitsOptions


class Window_MixtureCalculations(QtWidgets.QWidget, Ui_MixtureCalculationWindow):
    def __init__(self, parent=None):
        super(Window_MixtureCalculations, self).__init__(parent)
        self.setupUi(self)

        self.sname = " "
        self.eosname = " "

        # connect
        self.btn_Add.clicked.connect(self.add_substance_to_system)
        self.btn_Remove.clicked.connect(self.remove_substance_from_system)
        self.btn_Add.clicked.connect(self._changedSystem)
        self.btn_Remove.clicked.connect(self._changedSystem)
        self.btn_EditBIParameters.clicked.connect(self.edit_binary_parameters)
        self.btn_units.clicked.connect(self.open_units_options)
        self.btn_calculate.clicked.connect(self.calculateMixProperties)
        self.btn_savetxt.clicked.connect(self.save_to_txt)
        self.btn_SaveSystem.clicked.connect(self.saveSystem)
        self.btn_LoadSystem.clicked.connect(self.loadSystem)
        self.btn_VLE.clicked.connect(self.openVLEWindow)
        # self.tableWidget_MixtureSystem.itemChanged.connect(
        #     self._autoCompleteLastMolarFraction
        # )
        # self.btn_Add.clicked.connect(self._autoCompleteLastMolarFraction)
        # self.btn_Remove.clicked.connect(self._autoCompleteLastMolarFraction)

        # add combobox units options
        self.comboBox_procTunit.addItems(units.temperature_options)
        self.comboBox_refTunit.addItems(units.temperature_options)
        self.comboBox_procPunit.addItems(units.pressure_options)
        self.comboBox_refPunit.addItems(units.pressure_options)

        self.btn_searchSubstance.clicked.connect(self.search_substance)

        self.k = [[0, 0]]
        self.n = 0
        self.y = [0]
        self.subs_in_system = None
        self.mix = None
        self.eos = None
        self.eosname = None

        # results header
        self.ResultsColumnsLabels = ["Liquid", "Vapor"]
        self.tableWidget_results.setColumnCount(2)
        self.tableWidget_results.setHorizontalHeaderLabels(self.ResultsColumnsLabels)
        h_header = self.tableWidget_results.horizontalHeader()
        h_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        h_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # tablewidget -> database
        self.tableWidget_searchSubstance.itemSelectionChanged.connect(
            self.substance_selected
        )
        self.dbfile = db.database_file
        # 26 colunas
        self.units = {
            "P": "bar",
            "T": "K",
            "V": "m3/mol",
            "rho": "kg/m3",
            "energy_per_mol": "J/mol",
            "energy_per_mol_temp": "J/molK",
        }
        self.col_headers = [
            "Formula",
            "Name",
            "CAS #",
            "Mol. Wt.",
            "Tfp [K]",
            "Tb [K]",
            "Tc [K]",
            "Pc [bar]",
            "Vc [cm3/mol]",
            "Zc",
            "Omega",
            "T range (Cp) [K]",
            "a0",
            "a1",
            "a2",
            "a3",
            "a4",
            "Cp IG",
            "Cp liq.",
            "Antoine A",
            "Antoine B",
            "Antoine C",
            "Pvp min [bar]",
            "Tmin [K]",
            "Pvp max [bar]",
            "Tmax [K]",
        ]

        self.tableWidget_searchSubstance.setHorizontalHeaderLabels(self.col_headers)
        header = self.tableWidget_searchSubstance.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        self.load_db()
        self.le_searchSubstance.setFocus()
        self.database_changed = False

        # listview -> eos options
        self.listWidget_eos_options.addItems(list(eos.eos_options.keys()))
        self.listWidget_eos_options.itemSelectionChanged.connect(self.eos_selected)

    @QtCore.Slot()
    def calculateMixProperties(self):
        # get process variables (T and P)
        # get units

        if self.eosname is None:
            msg = QtWidgets.QMessageBox.about(self, "Error", "Please, select a EOS")
            return 1

        self.procTunit = self.comboBox_procTunit.currentText()
        self.procPunit = self.comboBox_procPunit.currentText()
        self.refTunit = self.comboBox_refTunit.currentText()
        self.refPunit = self.comboBox_refPunit.currentText()
        try:
            self.T = conv_unit(
                float(self.le_procT.text()), self.procTunit, "K"
            )  # convert to Kelvin
            self.P = conv_unit(
                float(self.le_procP.text()), self.procPunit, "Pa"
            )  # convert to pascal
            self.Tref = conv_unit(
                float(self.le_refT.text()), self.refTunit, "K"
            )  # convert to Kelvin
            self.Pref = conv_unit(
                float(self.le_refP.text()), self.refPunit, "Pa"
            )  # convert to pascal
        except:
            print("error process variables")
            msg = QtWidgets.QMessageBox.about(
                self, "Error", "Process variables are not numbers"
            )
            return 1

        # check if there's more than two components
        if self.n < 2:
            msg = QtWidgets.QMessageBox.about(
                self,
                "Mixture error",
                "Please, select a system with two or more substances",
            )
            return -1

        # TODO check if fraction sums to 1.0

        if not self._isMolarFractionSumOk():
            msg = QtWidgets.QMessageBox.about(
                self,
                "Mixture molar fraction error",
                "Molar fraction doesn't sum to one",
            )
            raise ("Molar fraction doesn't sum to one")

        # get all substances in the system, with all the respective molar fractions
        try:
            self._getVectorOfSubstancesInSystem()
            self._getSystemMolarFraction()
            self.mix = MixtureProp(self.subs_in_system, self.y)

        except Exception as err:
            msg = QtWidgets.QMessageBox.about(
                self, "Mixture error", "Couldn't create mixture \n" + str(err)
            )
            raise ("Mixture error")

        if self.eosname is not None:

            self.plainTextEdit_information.clear()
            self.tableWidget_results.setRowCount(0)
            self.plainTextEdit_log.clear()

            try:
                self.eoseq = EOS(self.mix, self.k, self.eosname)

                self.info = ""
                tab = "    "
                self.info += "Mixture:\n"

                for i in range(self.n):
                    n = self.subs_in_system[i].Name
                    f = self.subs_in_system[i].Formula
                    z = self.y[i]
                    self.info += tab + "{:} ({:}) [{:0.4f}]\n".format(n, f, z)

                self.info += "Equation of state: {0:s}\n".format(self.eosname)
                self.info += "Process state: {0:.3f} {1:s}, {2:s} {3:s}\n".format(
                    conv_unit(self.T, "K", self.units["T"]),
                    self.units["T"],
                    utils.f2str(
                        conv_unit(self.P, "Pa", self.units["P"]), 3, lt=1e-2, gt=1e4
                    ),
                    self.units["P"],
                )
                self.info += "Reference state: {0:.3f} {1:s}, {2:s} {3:s}\n".format(
                    conv_unit(self.Tref, "K", self.units["T"]),
                    self.units["T"],
                    utils.f2str(
                        conv_unit(self.Pref, "Pa", self.units["P"]), 3, lt=1e-2, gt=1e4
                    ),
                    self.units["P"],
                )
                self.plainTextEdit_information.appendPlainText(self.info)
            except Exception as e:
                print(e)
                err = (
                    "One or more of the following properties is not set: Tc, Pc, omega"
                )
                msg = QtWidgets.QMessageBox.about(self, "Properties error", str(err))
                return 1

            try:  # calculate properties at T and P

                self.propsliq, self.propsvap = self.eoseq.getAllProps(
                    self.Tref, self.T, self.Pref, self.P
                )
                self.Pvp = VaporPressure()
                self.log = self.propsliq.log

            except Exception as e:
                msg = QtWidgets.QMessageBox.about(
                    self, "Error calculating mixture properties", str(e)
                )
                return 1

            try:
                self.rowlabels, self.liq, self.vap = reports.tablewidget_vap_liq_reports(
                    self.propsliq, self.propsvap, self.Pvp, **self.units
                )
                for i in range(len(self.rowlabels)):
                    self.tableWidget_results.insertRow(i)
                    liqitem = QtWidgets.QTableWidgetItem(self.liq[i])
                    vapitem = QtWidgets.QTableWidgetItem(self.vap[i])
                    liqitem.setTextAlignment(QtCore.Qt.AlignRight)
                    vapitem.setTextAlignment(QtCore.Qt.AlignRight)
                    self.tableWidget_results.setItem(i, 0, liqitem)
                    self.tableWidget_results.setItem(i, 1, vapitem)
                self.tableWidget_results.setVerticalHeaderLabels(self.rowlabels)

            except Exception as e:
                msg = QtWidgets.QMessageBox.about(
                    self, "Error showing mixture results", str(e)
                )
                return 1

            try:
                self.plainTextEdit_log.appendPlainText(self.log)
            except Exception as e:
                print("Couldn't generate report")
                print(str(e))

    def _getVectorOfSubstancesInSystem(self):
        self.subs_in_system = []

        try:
            for i in range(self.n):
                name = self.tableWidget_MixtureSystem.item(i, 0).text()
                formula = self.tableWidget_MixtureSystem.item(i, 1).text()
                self.subs_in_system.append(SubstanceProp(name, formula))
        except Exception as err:
            msg = QtWidgets.QMessageBox.about(
                self,
                "Mixture error",
                "Couldn't create mixture from single substances\n" + str(err),
            )
            raise ("Mixture error")

    def _isMolarFractionSumOk(self):
        s = 0.0
        for i in range(self.n):
            s += float(self.tableWidget_MixtureSystem.item(i, 2).text())
        return np.allclose(1.0, s, 1e-5)

    @QtCore.Slot()
    def _autoCompleteLastMolarFraction(self):
        s = 1.0
        for i in range(self.n - 1):
            try:
                v = float(self.tableWidget_MixtureSystem.item(i, 2).text())
                t = v * 1.0 + 1.0
                s -= v
            except:
                pass
        item = QtWidgets.QTableWidgetItem(str(s))
        self.tableWidget_MixtureSystem.setItem(self.n - 1, 2, item)

    @QtCore.Slot()
    def edit_binary_parameters(self):
        components = []
        formulas = []
        for i in range(self.n):
            c = self.tableWidget_MixtureSystem.item(i, 0).text()
            f = self.tableWidget_MixtureSystem.item(i, 1).text()
            components.append(c)
            formulas.append(f)

        self.editBinPar = Window_BinaryInteractionParameters(
            components, formulas, self.k
        )
        self.editBinPar.return_k.connect(self._set_k)
        self.editBinPar.show()

    def _getSystemMolarFraction(self):
        self.y = np.empty(self.n, dtype=np.float64)
        for i in range(self.n):
            tmpn = self.tableWidget_MixtureSystem.item(i, 2).text()
            try:
                tmpn = float(tmpn)
                t = tmpn * 1.0 + 1.0
                self.y[i] = tmpn
            except:
                err = "Molar fractions are not valid numbers"
                msg = QtWidgets.QMessageBox.about(self, "Error", str(err))
                return -1

    @QtCore.Slot()
    def _set_k(self, k):
        self.k = k

    @QtCore.Slot()
    def _changedSystem(self):
        self.n = self.tableWidget_MixtureSystem.rowCount()
        self.k = np.zeros([self.n, self.n], dtype=np.float64)

    @QtCore.Slot()
    def add_substance_to_system(self):
        current_row = self.tableWidget_searchSubstance.currentRow()
        if current_row > -1:
            self.sname = self.tableWidget_searchSubstance.item(current_row, 1)
            self.sformula = self.tableWidget_searchSubstance.item(current_row, 0)
            rowpos = self.tableWidget_MixtureSystem.rowCount()
            self.tableWidget_MixtureSystem.insertRow(rowpos)
            self.tableWidget_MixtureSystem.setItem(
                rowpos, 0, QtWidgets.QTableWidgetItem(self.sname)
            )
            self.tableWidget_MixtureSystem.setItem(
                rowpos, 1, QtWidgets.QTableWidgetItem(self.sformula)
            )
            self.tableWidget_MixtureSystem.setItem(
                rowpos, 2, QtWidgets.QTableWidgetItem("0.0")
            )

    @QtCore.Slot()
    def remove_substance_from_system(self):
        current_row = self.tableWidget_MixtureSystem.currentRow()
        if current_row > -1:
            self.tableWidget_MixtureSystem.removeRow(current_row)

    @QtCore.Slot()
    def eos_selected(self):
        self.eosname = self.listWidget_eos_options.currentItem().text()

    @QtCore.Slot()
    def open_units_options(self):
        self.unitsOptionsWindow = Window_UnitsOptions(self.units)
        self.unitsOptionsWindow.return_units_dict.connect(self.set_units_dict)
        self.unitsOptionsWindow.show()

    @QtCore.Slot()
    def set_units_dict(self, dictionary):
        self.units = dictionary

    @QtCore.Slot()
    def save_to_txt(self):
        if self.plainTextEdit_information.toPlainText() == "":
            til = "No data"
            msg = "Please, generate the data first"
            QtWidgets.QMessageBox.about(self, til, msg)
            return
        try:
            name_suggestion = "mixture01" + ".txt"
            txt_file_name = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save file", name_suggestion, "Text files (*.txt)"
            )[0]
            if not txt_file_name:
                return 0
            report = self.generateReport()
            file_content = self.info + "\n\n" + report + "\n--- LOG ---\n" + self.log
            try:
                with open(txt_file_name, "w") as f:
                    f.write(file_content)
                til = "Successful"
                msg = "The data has been successfully saved."
            except Exception as e:
                til = "Problem"
                msg = "The data couldn't be saved.\n" + str(e)
            QtWidgets.QMessageBox.about(self, til, msg)

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
            QtWidgets.QMessageBox.about(self, til, msg)
            return -1

    def generateReport(self):
        report = ""

        def fmt(label, liq, vap):
            return "{:<25}\t{:>20}\t{:>20}\n".format(str(label), str(liq), str(vap))

        report += fmt("Properties", "Liquid", "Vapor")

        for i in range(len(self.rowlabels)):
            lbl = self.rowlabels[i]
            l = self.liq[i]
            v = self.vap[i]
            report += fmt(str(lbl), str(l), str(v))
        return report

    @QtCore.Slot()
    def saveSystem(self):
        if self.n < 2:
            til = "No mixture"
            msg = "Please, select two or more substances"
            QtWidgets.QMessageBox.about(self, til, msg)
            return

        import _devinfo

        try:
            _file_extension = _devinfo.__MIXTURESYSTEM_FILE_EXTENSION__
            name_suggestion = "mixture_system" + _file_extension
            txt_file_name = QtWidgets.QFileDialog.getSaveFileName(
                self,
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
                file_content += str(self.n) + "\n"
                file_content += "\n"

                self._getSystemMolarFraction()

                # Name, formula and molar fraction
                for i in range(self.n):
                    name = self.tableWidget_MixtureSystem.item(i, 0).text()
                    formula = self.tableWidget_MixtureSystem.item(i, 1).text()
                    file_content += '"{0:s}"\t"{1:s}"\t{2:0.8f}\n'.format(
                        name, formula, self.y[i]
                    )

                file_content += "\n"

                # binary interaction parameters
                for i in range(self.n):
                    for j in range(self.n - 1):
                        file_content += "{0:0.8f}\t".format(self.k[i][j])
                    file_content += "{0:0.8f}\n".format(self.k[i][self.n - 1])

                with open(txt_file_name, "w") as f:
                    f.write(file_content)
                til = "Successful"
                msg = "The system has been successfully saved."
            except Exception as e:
                til = "Error"
                msg = "The system couldn't be saved.\n" + str(e)
            QtWidgets.QMessageBox.about(self, til, msg)

        except Exception as e:
            til = "Error generating txt file"
            msg = str(e)
            QtWidgets.QMessageBox.about(self, til, msg)
            return -1

    @QtCore.Slot()
    def loadSystem(self):
        import _devinfo
        import shlex

        _file_extension = _devinfo.__MIXTURESYSTEM_FILE_EXTENSION__
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self,
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

            self.n = int(content[0])
            self.y = np.empty(self.n, dtype=np.float64)
            self.k = np.empty([self.n, self.n], dtype=np.float64)
            self.tableWidget_MixtureSystem.setRowCount(self.n)

            index = 1
            for i in range(self.n):
                subs = shlex.split(content[index + i])
                n = QtWidgets.QTableWidgetItem(subs[0])
                f = QtWidgets.QTableWidgetItem(subs[1])
                v = QtWidgets.QTableWidgetItem(subs[2])
                self.y[i] = float(subs[2])
                self.tableWidget_MixtureSystem.setItem(i, 0, n)
                self.tableWidget_MixtureSystem.setItem(i, 1, f)
                self.tableWidget_MixtureSystem.setItem(i, 2, v)

            index += self.n
            for i in range(self.n):
                for j in range(self.n):
                    ks = shlex.split(content[index + i])
                    self.k[i][j] = float(ks[j])

        except Exception as e:
            title = "Error loading system"
            msg = 'Error reading from file "' + filename + '"\n' + str(e)
            QtWidgets.QMessageBox.about(self, title, msg)

    def openVLEWindow(self):
        if self.n < 2:
            msg = QtWidgets.QMessageBox.about(
                self,
                "Mixture error",
                "Please, select a system with two or more substances",
            )
            return -1

        self._getVectorOfSubstancesInSystem()
        self._getSystemMolarFraction()

        self.vlewindow = Window_VLE(
            self.subs_in_system,
            self.y,
            self.k,
            self.le_procT.text(),
            self.comboBox_procTunit.currentText(),
            self.le_procP.text(),
            self.comboBox_procPunit.currentText(),
        )
        self.vlewindow.show()

    # ================== DB HANDLER ===========================
    def load_db(self):
        # Abrir banco de dados
        if os.path.isfile(self.dbfile):
            self.show_full_db()
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Database not found")
            error_dialog.exec_()
            raise Exception("Database not found")

    def show_full_db(self):
        try:
            query = "SELECT * FROM database"
            db.cursor.execute(query)
            results = db.cursor.fetchall()
            self.update_table_db(results)
        except:
            pass

    def update_table_db(self, results):
        self.tableWidget_searchSubstance.setRowCount(0)

        for row_number, row_data in enumerate(results):
            self.tableWidget_searchSubstance.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.tableWidget_searchSubstance.setItem(
                    row_number, col_number, QtWidgets.QTableWidgetItem(str(data))
                )

    def get_row_values(self, n):
        row_values = []
        current_row = self.tableWidget_searchSubstance.currentRow()

        for i in range(n):
            item = self.tableWidget_searchSubstance.item(current_row, i).text()
            row_values.append(item)

        return row_values

    @QtCore.Slot()
    def substance_selected(self):
        current_row = self.tableWidget_searchSubstance.currentRow()
        if current_row >= 0:
            r = self.get_row_values(10)
            self.compound = db_utils.get_compound_properties(r[1], r[0])
            self.sname = self.compound.getName()
            self.sformula = self.compound.getFormula()

    @QtCore.Slot()
    def search_substance(self):
        substance_string_name = str(self.le_searchSubstance.text())
        if substance_string_name == "":
            self.show_full_db()
        else:
            try:
                # query = "SELECT * FROM database WHERE Name LIKE '%" + substance_string_name + "%'" + \
                #         " OR Formula LIKE '%" + substance_string_name + "%'" + \
                #         " OR `CAS #` LIKE '%" + substance_string_name + "%'"
                query = (
                    "SELECT * FROM database WHERE Name LIKE '"
                    + substance_string_name
                    + "%'"
                    + " OR Formula LIKE '"
                    + substance_string_name
                    + "%'"
                    + " OR `CAS #` LIKE '"
                    + substance_string_name
                    + "%'"
                )
                db.cursor.execute(query)
                results = db.cursor.fetchall()
                self.update_table_db(results)
            except:
                self.tableWidget_searchSubstance.setRowCount(0)

    def clear_search(self):
        self.le_searchSubstance.clear()
        self.le_searchSubstance.setFocus()
