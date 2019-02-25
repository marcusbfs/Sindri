import os

from PySide2 import QtCore, QtWidgets

import PureSubstance
import db
import db_utils
import eos
import reports
import units
import utils
from pureSubstanceDiagramsWindow import Window_PureSubstanceDiagrams
from ui.pure_substance_calculations_ui import Ui_PureSubstanceCalculationsWindow
from units import conv_unit
from unitsOptionsWindow import Window_UnitsOptions


class Window_PureSubstanceCalculations(
    QtWidgets.QWidget, Ui_PureSubstanceCalculationsWindow
):
    def __init__(self, parent=None):
        super(Window_PureSubstanceCalculations, self).__init__(parent)
        self.setupUi(self)

        self.btn_searchSubstance.clicked.connect(self.search_substance)
        self.btn_calculate.clicked.connect(self.calculatePureSubstance)
        self.btn_diagrams.clicked.connect(self.open_diagrams)
        self.btn_savetxt.clicked.connect(self.save_to_txt)
        self.btn_units.clicked.connect(self.open_units_options)

        self.sname = " "
        self.eosname = " "

        # add combobox units options
        self.comboBox_procTunit.addItems(units.temperature_options)
        self.comboBox_refTunit.addItems(units.temperature_options)
        self.comboBox_procPunit.addItems(units.pressure_options)
        self.comboBox_refPunit.addItems(units.pressure_options)

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
    def calculatePureSubstance(self):
        # get process variables (T and P)
        # get units
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
            # TODO
            print("error process variables")
            msg = QtWidgets.QMessageBox.about(
                self, "Error", "Process variables are not numbers"
            )
            return 1

        if len(self.sname.strip()) > 1 and len(self.eosname.strip()) > 1:

            _decimals = 7
            _lt = 1e-3
            _gt = 1e4

            self.plainTextEdit_information.clear()
            self.tableWidget_results.setRowCount(0)
            self.plainTextEdit_log.clear()

            try:  # to initialize EOS
                self.c = PureSubstance.PureSubstance(
                    self.compound["Name"],
                    self.compound["Formula"],
                    eos.eos_options[self.eosname],
                )
                self.info = ""
                self.info += "Compound: {:s} ({:s})\n".format(
                    self.c.compound["Name"], self.c.compound["Formula"]
                )

                self.info += "Equation of state: {0:s}\n".format(
                    self.listWidget_eos_options.currentItem().text()
                )
                self.info += "Process state: {0:.3f} {1:s}, {2:s} {3:s}\n".format(
                    conv_unit(self.T, "K", self.units["T"]),
                    self.units["T"],
                    utils.f2str(
                        conv_unit(self.P, "Pa", self.units["P"]), 3, lt=1e-2, gt=1e4
                    ),
                    self.units["P"],
                )
                self.info += "Reference state: {0:.3f} {1:s}, {2:s} {3:s}".format(
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
                msg = QtWidgets.QMessageBox.about(self, "Error", str(err))
                return 1

            try:  # calculate properties at T and P
                self.props = self.c.all_calculations_at_P_T(
                    self.P, self.T, self.Pref, self.Tref
                )
                self.plainTextEdit_information.appendPlainText(
                    "State: " + self.props.state
                )

            except Exception as e:
                msg = QtWidgets.QMessageBox.about(
                    self, "Error calculating properties", str(e)
                )
                return 1

            try:
                rowlabels, liq, vap = reports.tablewidget_vap_liq_reports(
                    self.props, **self.units
                )
                for i in range(len(rowlabels)):
                    self.tableWidget_results.insertRow(i)
                    liqitem = QtWidgets.QTableWidgetItem(liq[i])
                    vapitem = QtWidgets.QTableWidgetItem(vap[i])
                    liqitem.setTextAlignment(QtCore.Qt.AlignRight)
                    vapitem.setTextAlignment(QtCore.Qt.AlignRight)
                    self.tableWidget_results.setItem(i, 0, liqitem)
                    self.tableWidget_results.setItem(i, 1, vapitem)
                self.tableWidget_results.setVerticalHeaderLabels(rowlabels)

            except Exception as e:
                msg = QtWidgets.QMessageBox.about(self, "Error showing results", str(e))
                return 1

            try:
                self.report, self.log = reports.format_reports(self.props, **self.units)
                self.plainTextEdit_log.appendPlainText(self.log)
            except Exception as e:
                print("Couldn't generate report")
                print(str(e))

        else:
            msg = QtWidgets.QMessageBox.about(
                self, "Error", "Please, select compound and EOS"
            )
            return

    @QtCore.Slot()
    def open_diagrams(self):
        if len(self.sname.strip()) > 1 and len(self.eosname.strip()) > 1:

            _decimals = 7
            _lt = 1e-3
            _gt = 1e4

            try:  # to initialize EOS
                self.c = PureSubstance.PureSubstance(
                    self.compound["Name"],
                    self.compound["Formula"],
                    eos.eos_options[self.eosname],
                )
            except:
                err = (
                    "One or more of the following properties is not set: Tc, Pc, omega"
                )
                msg = QtWidgets.QMessageBox.about(self, "Error", str(err))
                return 1

            self.refTunit = self.comboBox_refTunit.currentText()
            self.refPunit = self.comboBox_refPunit.currentText()

            try:
                self.Tref = conv_unit(
                    float(self.le_refT.text()), self.refTunit, "K"
                )  # convert to Kelvin
                self.Pref = conv_unit(
                    float(self.le_refP.text()), self.refPunit, "Pa"
                )  # convert to pascal
            except Exception as e:
                print(str(e))
                msg = QtWidgets.QMessageBox.about(
                    self, "Error", "Reference state variables are not numbers"
                )
                return -1

            self.diagramsWindow = Window_PureSubstanceDiagrams(
                self.c, self.Pref, self.Tref
            )
            self.diagramsWindow.show()

        else:
            msg = QtWidgets.QMessageBox.about(
                self, "Error", "Please, select compound and EOS"
            )
            return

    @QtCore.Slot()
    def open_units_options(self):
        self.unitsOptionsWindow = Window_UnitsOptions()
        self.unitsOptionsWindow.return_units_dict.connect(self.set_units_dict)
        self.unitsOptionsWindow.show()

    @QtCore.Slot()
    def set_units_dict(self, dictionary):
        self.units = dictionary

    @QtCore.Slot()
    def save_to_txt(self):
        try:
            name_suggestion = self.c.compound["Name"] + ".txt"
            txt_file_name = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save file", name_suggestion, "Text files (*.txt)"
            )[0]
            if not txt_file_name:
                return 0
            file_content = self.info + self.report + "\n--- LOG ---\n" + self.log
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
                til = "Error"
                msg = str(e)
            QtWidgets.QMessageBox.about(self, til, msg)
            return -1

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
    def eos_selected(self):
        self.eosname = self.listWidget_eos_options.currentItem().text()

    @QtCore.Slot()
    def substance_selected(self):
        current_row = self.tableWidget_searchSubstance.currentRow()
        if current_row >= 0:
            r = self.get_row_values(10)
            self.compound = db_utils.get_compound_properties(r[1], r[0])
            self.sname = self.compound["Name"] + " (" + self.compound["Formula"] + ")"

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
