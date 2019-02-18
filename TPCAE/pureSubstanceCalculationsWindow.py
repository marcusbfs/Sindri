import os

import numpy as np
from PySide2 import QtCore, QtWidgets

import IdealGasPropertiesPureSubstance as IGprop
import antoineVP
import db
import db_utils
import eos
import units
from units import conv_unit
import utils
from constants import R_IG
from ui.pure_substance_calculations_ui import Ui_PureSubstanceCalculationsWindow


class Window_PureSubstanceCalculations(QtWidgets.QWidget, Ui_PureSubstanceCalculationsWindow):

    def __init__(self, parent=None):
        super(Window_PureSubstanceCalculations, self).__init__(parent)
        self.setupUi(self)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.btn_searchSubstance.clicked.connect(self.search_substance)
        self.btn_calculate.clicked.connect(self.calculatePureSubstance)

        self.sname = " "
        self.eosname = " "

        # add combobox units options
        self.comboBox_procTunit.addItems(units.temperature_options)
        self.comboBox_refTunit.addItems(units.temperature_options)
        self.comboBox_procPunit.addItems(units.pressure_options)
        self.comboBox_refPunit.addItems(units.pressure_options)

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
        # get units
        self.procTunit = self.comboBox_procTunit.currentText()
        self.procPunit = self.comboBox_procPunit.currentText()
        self.refTunit = self.comboBox_refTunit.currentText()
        self.refPunit = self.comboBox_refPunit.currentText()
        try:
            self.T = conv_unit(float(self.le_procT.text()), self.procTunit, "K")  # convert to Kelvin
            self.P = conv_unit(float(self.le_procP.text()), self.procPunit, "Pa")  # convert to pascal
            self.Tref = conv_unit(float(self.le_refT.text()), self.refTunit, "K")  # convert to Kelvin
            self.Pref = conv_unit(float(self.le_refP.text()), self.refPunit, "Pa")  # convert to pascal
        except:
            # TODO
            print("error process variables")
            msg = QtWidgets.QMessageBox.about(self, "Error", "Process variables are not numbers")
            return 1

        if len(self.sname.strip()) > 1 and len(self.eosname.strip()) > 1:

            _decimals = 7
            _lt = 1e-3
            _gt = 1e4

            self.plainTextEdit_results.clear()

            try:  # to initialize EOS
                self.c = eos.EOS(self.compound["Name"], self.compound["Formula"], eos.eos_options[self.eosname])
                self.plainTextEdit_results.appendPlainText("compound: {:s} ({:s})".format(
                    self.c.compound["Name"], self.c.compound["Formula"]
                ))
                self.plainTextEdit_results.appendPlainText(
                    "equation of state: {0:s}".format(self.listWidget_eos_options.currentItem().text()))
                self.plainTextEdit_results.appendPlainText(
                    "process state: {:.3f} K, {:s} bar".format(self.T,
                                                               utils.f2str(conv_unit(self.P, "Pa", "bar"), 3, lt=1e-2,
                                                                           gt=1e4))
                )
                self.plainTextEdit_results.appendPlainText(
                    "reference state: {:.3f} K, {:s} bar".format(self.Tref,
                                                                 utils.f2str(conv_unit(self.Pref, "Pa", "bar"), 3,
                                                                             lt=1e-2, gt=1e4))
                )
            except Exception as e:
                err = "One or more of the following properties is not set: Tc, Pc, omega"
                msg = QtWidgets.QMessageBox.about(self, "Error", str(err))
                return 1

            try:  # calculate Zc and Vc
                self.Zs = self.c.return_Z_given_PT(self.P, self.T)
                self.Zliq = np.min(self.Zs)
                self.Zvap = np.max(self.Zs)
                self.Vliq = self.T * R_IG * self.Zliq / self.P
                self.Vvap = self.T * R_IG * self.Zvap / self.P

                self.Zsref = self.c.return_Z_given_PT(self.Pref, self.Tref)
                self.Zliqref = np.min(self.Zsref)
                self.Zvapref = np.max(self.Zsref)
                self.Vliqref = self.Tref * R_IG * self.Zliqref / self.Pref
                self.Vvapref = self.Tref * R_IG * self.Zvapref / self.Pref

                self.minVs = utils.f2str(self.Vliq, _decimals, _lt, _gt)
                self.maxVs = utils.f2str(self.Vvap, _decimals, _lt, _gt)
                self.minZs = utils.f2str(self.Zliq, _decimals, _lt, _gt)
                self.maxZs = utils.f2str(self.Zvap, _decimals, _lt, _gt)
                # add to plain text editor
                self.plainTextEdit_results.appendPlainText("Vc [m3/mol]: " + self.minVs + " (liquid), " +
                                                           self.maxVs + " (vapor)")
                self.plainTextEdit_results.appendPlainText("Zc: " + self.minZs + " (liquid), " +
                                                           self.maxZs + " (vapor)")
            except Exception as e:
                msg = QtWidgets.QMessageBox.about(self, "Error", str(e))
                return 1

            # print(self.Vs)
            # print(self.Zs)
            if self.compound["Mol. Wt."] is not None:
                self.rholiq = self.compound["Mol. Wt."] * 1e-3 / self.Vliq  # all densisties are in kg/m3
                self.rhovap = self.compound["Mol. Wt."] * 1e-3 / self.Vvap
                maxrhos = utils.f2str(self.rholiq, _decimals, _lt, _gt)
                minrhos = utils.f2str(self.rhovap, _decimals, _lt, _gt)
                # self.tableWidget_results.setItem(2, 0, QtWidgets.QTableWidgetItem(maxrhos))
                # self.tableWidget_results.setItem(2, 1, QtWidgets.QTableWidgetItem(minrhos))
                self.plainTextEdit_results.appendPlainText("Density [kg/m3]: " + maxrhos + " (liquid), " +
                                                           minrhos + " (vapor)")
            else:
                # TODO
                print("error calculating densities")

            # TODO calcular Pvp antoine depois de Pvp eos?
            # Calculate Pvp - antoine
            if self.compound["ANTOINE_A"] and self.compound["ANTOINE_C"] and self.compound["ANTOINE_B"]:
                ans_antoine = antoineVP.antoineVP(self.T, self.compound["ANTOINE_A"], self.compound["ANTOINE_B"],
                                                  self.compound["ANTOINE_C"],
                                                  self.compound["Tmin_K"], self.compound["Tmax_K"])
                self.P_antoine = conv_unit(ans_antoine.Pvp, "bar", "Pa")
                displayP_antoine = utils.f2str(conv_unit(self.P_antoine, "Pa", "bar"), _decimals, _lt, _gt) + " bar"
                if ans_antoine[1]:
                    displayP_antoine = displayP_antoine + " (" + ans_antoine[1] + ")"
                self.plainTextEdit_results.appendPlainText("Pvp (Antoine): " + displayP_antoine)

                try:
                    self.state = IGprop.return_fluidState(self.P, conv_unit(self.compound["Pc_bar"], "bar", "Pa"),
                                                          self.T, self.compound["Tc_K"], self.P_antoine)
                    self.plainTextEdit_results.appendPlainText("fluid state: " + self.state)
                except:
                    # TODO
                    print("error calculating fluid state")

            # calculate Ideal Properties
            if self.compound["a0"] is not None and self.compound["a1"] is not None and self.compound[
                "a2"] is not None and self.compound["a3"] is not None and \
                    self.compound["a4"] is not None:
                a0 = self.compound["a0"]
                a1 = self.compound["a1"]
                a2 = self.compound["a2"]
                a3 = self.compound["a3"]
                a4 = self.compound["a4"]
                _gt = 1e5

                try:
                    self.IG_properties = IGprop.return_IdealGasProperties(self.Tref, self.T, self.Pref, self.P,
                                                                          a0, a1, a2, a3, a4,
                                                                          self.c.compound["Tcpmin_K"],
                                                                          self.c.compound["Tcpmax_K"]
                                                                          )
                    self.Cp_IG = self.IG_properties["Cp_IG"]
                    self.dH_IG = self.IG_properties["dH_IG"]
                    self.dG_IG = self.IG_properties["dG_IG"]
                    self.dU_IG = self.IG_properties["dU_IG"]
                    self.dS_IG = self.IG_properties["dS_IG"]
                    self.dA_IG = self.IG_properties["dA_IG"]

                    Cpstr = utils.f2str(self.Cp_IG, _decimals, _lt, _gt)
                    Hstr = utils.f2str(self.dH_IG, _decimals, _lt, _gt)
                    Astr = utils.f2str(self.dA_IG, _decimals, _lt, _gt)
                    Sstr = utils.f2str(self.dS_IG, _decimals, _lt, _gt)
                    Ustr = utils.f2str(self.dU_IG, _decimals, _lt, _gt)
                    Gstr = utils.f2str(self.dG_IG, _decimals, _lt, _gt)

                    if self.IG_properties["msg"] is not None:
                        self.plainTextEdit_results.appendPlainText("Cp calculation is out of bound ({:s})".format(msg))

                    self.plainTextEdit_results.appendPlainText("Cp at T [J mol-1 K-1]: " + Cpstr)
                    self.plainTextEdit_results.appendPlainText("dH_IG [J mol-1]: " + Hstr)
                    self.plainTextEdit_results.appendPlainText("dS_IG [J mol-1 K-1]: " + Sstr)
                    self.plainTextEdit_results.appendPlainText("dG_IG [J mol-1]: " + Gstr)
                    self.plainTextEdit_results.appendPlainText("dU_IG [J mol-1]: " + Ustr)
                    self.plainTextEdit_results.appendPlainText("dA_IG [J mol-1]: " + Astr)

                except:
                    print("error calculating ideal gas properties")

                # calculating departure functions and residual properties
                try:

                    self.residualDelta_vap = self.c.return_delta_ResProperties(self.Pref, self.Tref, self.Vvapref,
                                                                               self.Zvapref,
                                                                               self.P, self.T, self.Vvap, self.Zvap)

                    self.residualDelta_liq = self.c.return_delta_ResProperties(self.Pref, self.Tref, self.Vliqref,
                                                                               self.Zliqref,
                                                                               self.P, self.T, self.Vliq, self.Zliq)

                    self.dH_vap = self.dH_IG - self.residualDelta_vap["HR"]
                    self.dS_vap = self.dS_IG - self.residualDelta_vap["SR"]
                    self.dG_vap = self.dG_IG - self.residualDelta_vap["GR"]
                    self.dU_vap = self.dU_IG - self.residualDelta_vap["UR"]
                    self.dA_vap = self.dA_IG - self.residualDelta_vap["AR"]
                    self.fugacity_vap = self.residualDelta_vap["f"]

                    self.dH_liq = self.dH_IG - self.residualDelta_liq["HR"]
                    self.dS_liq = self.dS_IG - self.residualDelta_liq["SR"]
                    self.dG_liq = self.dG_IG - self.residualDelta_liq["GR"]
                    self.dU_liq = self.dU_IG - self.residualDelta_liq["UR"]
                    self.dA_liq = self.dA_IG - self.residualDelta_liq["AR"]
                    self.fugacity_liq = self.residualDelta_liq["f"]

                    Hstr = utils.f2str(self.dH_liq, _decimals, _lt, _gt) + " (liq.), " + utils.f2str(
                        self.dH_vap, _decimals, _lt, _gt) + " (vap.)"
                    Sstr = utils.f2str(self.dS_liq, _decimals, _lt, _gt) + " (liq.), " + utils.f2str(
                        self.dS_vap, _decimals, _lt, _gt) + " (vap.)"
                    Gstr = utils.f2str(self.dG_liq, _decimals, _lt, _gt) + " (liq.), " + utils.f2str(
                        self.dG_vap, _decimals, _lt, _gt) + " (vap.)"
                    Ustr = utils.f2str(self.dU_liq, _decimals, _lt, _gt) + " (liq.), " + utils.f2str(
                        self.dU_vap, _decimals, _lt, _gt) + " (vap.)"
                    Astr = utils.f2str(self.dA_liq, _decimals, _lt, _gt) + " (liq.), " + utils.f2str(
                        self.dA_vap, _decimals, _lt, _gt) + " (vap.)"
                    fstr = utils.f2str(conv_unit(self.fugacity_liq, "Pa", "bar"), _decimals, 10 ** (2 - _decimals),
                                       _gt) + " (liq.), " + utils.f2str(conv_unit(self.fugacity_vap, "Pa", "bar"),
                                                                        _decimals, 10 ** (2 - _decimals),
                                                                        _gt) + " (vap.)"

                    self.plainTextEdit_results.appendPlainText("dH [J mol-1]: " + Hstr)
                    self.plainTextEdit_results.appendPlainText("dS [J mol-1 K-1]: " + Sstr)
                    self.plainTextEdit_results.appendPlainText("dG [J mol-1]: " + Gstr)
                    self.plainTextEdit_results.appendPlainText("dU [J mol-1]: " + Ustr)
                    self.plainTextEdit_results.appendPlainText("dA [J mol-1]: " + Astr)
                    self.plainTextEdit_results.appendPlainText("fugacity [bar]: " + fstr)

                except:
                    print("error calculating residual properties")

                # Pvp from EOS
                try:
                    tol = 1e-4
                    maxit = 100
                    try:
                        Pvp_eos_ret = self.c.return_Pvp_EOS(self.T, self.P_antoine, tol=tol, k=maxit)  # Pa

                    except:
                        Pvp_eos_ret = self.c.return_Pvp_EOS(self.T, conv_unit(1, "bar", "Pa"), tol=tol,
                                                            k=maxit)  # Pa
                    self.Pvp_eos = Pvp_eos_ret.Pvp
                    k = Pvp_eos_ret.msg
                    msg = "Pvp (EOS) [bar]: " + utils.f2str(conv_unit(self.Pvp_eos, "Pa", "bar"), 4,
                                                            lt=_lt) + " - iterations: " + str(k)
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    print("error calculating Pvp from EOS")

        else:
            msg = QtWidgets.QMessageBox.about(self, "Error", "Please, select compound and EOS")
            return

    @QtCore.Slot()
    def eos_selected(self):
        self.eosname = self.listWidget_eos_options.currentItem().text()
        # self.update_status_bar()

    @QtCore.Slot()
    def substance_selected(self):
        current_row = self.tableWidget_searchSubstance.currentRow()
        if current_row >= 0:
            r = self.get_row_values(10)
            self.compound = db_utils.get_compound_properties(r[1], r[0])
            self.sname = self.compound["Name"] + " (" + self.compound["Formula"] + ")"
            # self.update_status_bar()

    @QtCore.Slot()
    def search_substance(self):
        substance_string_name = str(self.le_searchSubstance.text())
        if substance_string_name == '':
            self.show_full_db()
        else:
            try:
                # query = "SELECT * FROM database WHERE Name LIKE '%" + substance_string_name + "%'" + \
                #         " OR Formula LIKE '%" + substance_string_name + "%'" + \
                #         " OR `CAS #` LIKE '%" + substance_string_name + "%'"
                query = "SELECT * FROM database WHERE Name LIKE '" + substance_string_name + "%'" + \
                        " OR Formula LIKE '" + substance_string_name + "%'" + \
                        " OR `CAS #` LIKE '" + substance_string_name + "%'"
                db.cursor.execute(query)
                results = db.cursor.fetchall()
                self.update_table_db(results)
            except:
                self.tableWidget_searchSubstance.setRowCount(0)

    # def update_status_bar(self):
    #     return
    #     self.statusbar.showMessage("Selected - substance: " + self.sname +
    #                                "; EOS: " + self.eosname)

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
