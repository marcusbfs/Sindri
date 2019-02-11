import numpy as np
import os
from PySide2 import QtCore, QtWidgets
from ui.pure_substance_calculations_ui import Ui_PureSubstanceCalculationsWindow
import db
import db_utils
import utils
import eos
import antoineVP
import units


class Window_PureSubstanceCalculations(QtWidgets.QWidget, Ui_PureSubstanceCalculationsWindow):

    def __init__(self, parent=None):
        super(Window_PureSubstanceCalculations, self).__init__(parent)
        self.setupUi(self)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.btn_searchSubstance.clicked.connect(self.search_substance)
        self.btn_calculate.clicked.connect(self.calculatePureSubstance)

        # self.statusbar.setObjectName("statusbar")
        # self.setStatusBar(self.statusbar)

        self.sname = " "
        self.eosname = " "

        # tablewidget -> database
        self.tableWidget_searchSubstance.itemSelectionChanged.connect(self.substance_selected)
        self.dbfile = db.database_file
        # 26 colunas
        self.col_headers = ["Formula", "Name", "CAS #", "Mol. Wt.", "Tfp [K]", "Tb [K]",
                            "Tc [K]", "Pc [bar]", "Vc [cm3/mol]", "Zc", "Omega", "T range (Cp) [K]",
                            "a0", "a1", "a2", "a3", "a4", "Cp IG", "Cp liq.", "Antoine A",
                            "Antoine B", "Antoine C", "Pvp min [bar]", "Tmin [K]", "Pvp max [bar]", "Tmax [K]"]

        self.tableWidget_searchSubstance.setHorizontalHeaderLabels(self.col_headers)
        header = self.tableWidget_searchSubstance.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.load_db()
        self.le_searchSubstance.setFocus()
        self.database_changed = False

        # listview -> eos options
        self.listWidget_eos_options.addItems(list(eos.eos_options.keys()))
        self.listWidget_eos_options.itemSelectionChanged.connect(self.eos_selected)

    @QtCore.Slot()
    def calculatePureSubstance(self):
        # get process variables (T and P)
        try:
            self.T = float(self.le_procT.text())
            self.P = float(self.le_procP.text()) * units.bar_to_Pa  # convert to pascal
        except:
            # TODO
            print("error process variables")
            msg = QtWidgets.QMessageBox.about(self, "Error", "Process variables are not numbers")
            return 1

        if len(self.sname.strip()) > 1 and len(self.eosname.strip()) > 1:

            _decimals = 7
            _lt = 1e-3
            _gt = 1e4

            try:  # to initialize EOS
                self.c = eos.EOS(self.compound["Name"], self.compound["Formula"], eos.eos_options[self.eosname], self.T,
                                 self.P)
            except Exception as e:
                err = "One or more of the following properties is not set: Tc, Pc, omega"
                msg = QtWidgets.QMessageBox.about(self, "Error", str(err))
                return 1

            try:  # calculate Zc and Vc
                self.Zs = self.c.return_Z()
                self.Vs = self.c.return_V()
                # add to tablewidget
                minVs = utils.float2str(np.min(self.Vs), _decimals, _lt, _gt)
                maxVs = utils.float2str(np.max(self.Vs), _decimals, _lt, _gt)
                minZs = utils.float2str(np.min(self.Zs), _decimals, _lt, _gt)
                maxZs = utils.float2str(np.max(self.Zs), _decimals, _lt, _gt)
                self.tableWidget_results.setItem(0, 0, QtWidgets.QTableWidgetItem(minVs))
                self.tableWidget_results.setItem(0, 1, QtWidgets.QTableWidgetItem(maxVs))
                self.tableWidget_results.setItem(1, 0, QtWidgets.QTableWidgetItem(minZs))
                self.tableWidget_results.setItem(1, 1, QtWidgets.QTableWidgetItem(maxZs))
                # add to plain text editor
                self.plainTextEdit_results.appendPlainText("Vc [m3/mol]: " + minVs + " (liquid), " +
                                                           maxVs + " (vapor)")
                self.plainTextEdit_results.appendPlainText("Zc: " + minZs + " (liquid), " +
                                                           maxZs + " (vapor)")
            except Exception as e:
                msg = QtWidgets.QMessageBox.about(self, "Error", str(e))
                return 1

            # print(self.Vs)
            # print(self.Zs)
            if self.compound["Mol. Wt."]:
                self.rhos = self.compound["Mol. Wt."] * 1e-3 / self.Vs
                maxrhos = utils.float2str(np.max(self.rhos), _decimals, _lt, _gt)
                minrhos = utils.float2str(np.min(self.rhos), _decimals, _lt, _gt)
                self.tableWidget_results.setItem(2, 0, QtWidgets.QTableWidgetItem(maxrhos))
                self.tableWidget_results.setItem(2, 1, QtWidgets.QTableWidgetItem(minrhos))
                self.plainTextEdit_results.appendPlainText("Density [kg/m3]: " + maxrhos + " (liquid), " +
                                                           minrhos + " (vapor)")
            else:
                self.rhos = ["", ""]

            if self.compound["ANTOINE_A"] and self.compound["ANTOINE_C"] and self.compound["ANTOINE_B"]:
                ans_antoine = antoineVP.antoineVP(self.T, self.compound["ANTOINE_A"], self.compound["ANTOINE_B"],
                                                  self.compound["ANTOINE_C"],
                                                  self.compound["Tmin_K"], self.compound["Tmax_K"])
                self.P_antoine = ans_antoine[0] * units.bar_to_Pa
                displayP_antoine = utils.float2str(self.P_antoine, _decimals, _lt, _gt)
                if ans_antoine[1]:
                    displayP_antoine = displayP_antoine + " (" + ans_antoine[1] + ")"
                self.plainTextEdit_results.appendPlainText("Pvp (Antoine) [Pa]:" + displayP_antoine)

        else:
            msg = QtWidgets.QMessageBox.about(self, "Error", "Please, select compound and EOS")
            return

    @QtCore.Slot()
    def eos_selected(self):
        self.eosname = self.listWidget_eos_options.currentItem().text()
        self.update_status_bar()

    @QtCore.Slot()
    def substance_selected(self):
        current_row = self.tableWidget_searchSubstance.currentRow()
        if current_row >= 0:
            r = self.get_row_values(10)
            self.compound = db_utils.get_compound_properties(r[1], r[0])
            self.sname = self.compound["Name"] + " (" + self.compound["Formula"] + ")"
            self.update_status_bar()

    @QtCore.Slot()
    def search_substance(self):
        substance_string_name = str(self.le_searchSubstance.text())
        if substance_string_name == '':
            self.show_full_db()
        else:
            try:
                query = "SELECT * FROM database WHERE Name LIKE '%" + substance_string_name + "%'" + \
                        " OR Formula LIKE '%" + substance_string_name + "%'" + \
                        " OR `CAS #` LIKE '%" + substance_string_name + "%'"
                db.cursor.execute(query)
                results = db.cursor.fetchall()
                self.update_table_db(results)
            except:
                self.tableWidget_searchSubstance.setRowCount(0)

    def update_status_bar(self):
        return
        self.statusbar.showMessage("Selected - substance: " + self.sname +
                                   "; EOS: " + self.eosname)

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
                self.tableWidget_searchSubstance.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))

    def get_row_values(self, n):

        row_values = []
        current_row = self.tableWidget_searchSubstance.currentRow()

        for i in range(n):
            item = self.tableWidget_searchSubstance.item(current_row, i).text()
            row_values.append(item)

        return row_values

    def clear_search(self):
        self.le_searchSubstance.clear()
        self.le_searchSubstance.setFocus()
