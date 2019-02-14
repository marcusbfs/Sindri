import os

import numpy as np
from PySide2 import QtCore, QtWidgets

import IdealGasPropertiesPureSubstance as IGprop
import antoineVP
import db
import db_utils
import eos
import units
import utils
from ui.pure_substance_calculations_ui import Ui_PureSubstanceCalculationsWindow


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
        # get units
        self.procTunit = self.comboBox_procTunit.currentText()
        self.procPunit = self.comboBox_procPunit.currentText()
        self.refTunit = self.comboBox_refTunit.currentText()
        self.refPunit = self.comboBox_refPunit.currentText()
        try:
            self.T = units.convert_to_SI("temperature", float(self.le_procT.text()),
                                         self.procTunit)  # convert to Kelvin
            self.P = units.convert_to_SI("pressure", float(self.le_procP.text()), self.procPunit)  # convert to pascal
            self.Tref = units.convert_to_SI("temperature", float(self.le_refT.text()),
                                            self.refTunit)  # convert to Kelvin
            self.Pref = units.convert_to_SI("pressure", float(self.le_refP.text()), self.refPunit)  # convert to pascal
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
                self.minVs = utils.float2str(np.min(self.Vs), _decimals, _lt, _gt)
                self.maxVs = utils.float2str(np.max(self.Vs), _decimals, _lt, _gt)
                self.minZs = utils.float2str(np.min(self.Zs), _decimals, _lt, _gt)
                self.maxZs = utils.float2str(np.max(self.Zs), _decimals, _lt, _gt)
                # self.tableWidget_results.setItem(0, 0, QtWidgets.QTableWidgetItem(self.minVs))
                # self.tableWidget_results.setItem(0, 1, QtWidgets.QTableWidgetItem(self.maxVs))
                # self.tableWidget_results.setItem(1, 0, QtWidgets.QTableWidgetItem(self.minZs))
                # self.tableWidget_results.setItem(1, 1, QtWidgets.QTableWidgetItem(self.maxZs))
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
            if self.compound["Mol. Wt."]:
                self.rhos = self.compound["Mol. Wt."] * 1e-3 / self.Vs
                maxrhos = utils.float2str(np.max(self.rhos), _decimals, _lt, _gt)
                minrhos = utils.float2str(np.min(self.rhos), _decimals, _lt, _gt)
                # self.tableWidget_results.setItem(2, 0, QtWidgets.QTableWidgetItem(maxrhos))
                # self.tableWidget_results.setItem(2, 1, QtWidgets.QTableWidgetItem(minrhos))
                self.plainTextEdit_results.appendPlainText("Density [kg/m3]: " + maxrhos + " (liquid), " +
                                                           minrhos + " (vapor)")
            else:
                self.rhos = ["", ""]

            # Calculate Pvp - antoine
            if self.compound["ANTOINE_A"] and self.compound["ANTOINE_C"] and self.compound["ANTOINE_B"]:
                ans_antoine = antoineVP.antoineVP(self.T, self.compound["ANTOINE_A"], self.compound["ANTOINE_B"],
                                                  self.compound["ANTOINE_C"],
                                                  self.compound["Tmin_K"], self.compound["Tmax_K"])
                self.P_antoine = ans_antoine[0] * units.bar_to_Pa
                displayP_antoine = utils.float2str(self.P_antoine * units.Pa_to_bar, _decimals, _lt, _gt) + " bar"
                if ans_antoine[1]:
                    displayP_antoine = displayP_antoine + " (" + ans_antoine[1] + ")"
                self.plainTextEdit_results.appendPlainText("Pvp (Antoine): " + displayP_antoine)

                try:
                    self.state = IGprop.return_fluidState(self.P, self.compound["Pc_bar"] * units.bar_to_Pa,
                                                          self.T, self.compound["Tc_K"],
                                                          self.P_antoine)
                    self.plainTextEdit_results.appendPlainText("fluid state: " + self.state)
                except:
                    # TODO
                    print("error calculating fluid state")

            # calculate cp and
            if self.compound["a0"] is not None and self.compound["a1"] is not None and self.compound[
                "a2"] is not None and self.compound["a3"] is not None and \
                    self.compound["a4"] is not None:
                a0 = self.compound["a0"]
                a1 = self.compound["a1"]
                a2 = self.compound["a2"]
                a3 = self.compound["a3"]
                a4 = self.compound["a4"]
                _gt = 1e5

                # cp
                try:
                    self.Cp = IGprop.return_Cp(self.T, a0, a1, a2, a3, a4)
                    msg = "Cp at T=" + str(self.T) + " [J mol-1 K-1]: " + utils.float2str(self.Cp, 4, lt=_lt, gt=_gt)
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    # TODO
                    print("error calculating Cp")
                # deltaH_IG
                try:
                    self.deltaH_IG = IGprop.return_deltaH_IG(self.Tref, self.T, a0, a1, a2, a3, a4)
                    msg = "deltaH_IG " + " [J mol-1]: " + utils.float2str(self.deltaH_IG, 4, lt=_lt, gt=_gt)
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    # TODO
                    print("error calculating deltaH_IG")

                # deltaH
                try:
                    self.minVs = np.min(self.Vs)
                    self.maxVs = np.max(self.Vs)
                    self.minZs = np.min(self.Zs)
                    self.maxZs = np.max(self.Zs)

                    HRproc_vap = self.c.return_HR_given_VT(self.P, self.T, "vap")
                    HRref_vap = self.c.return_HR_given_VT(self.Pref, self.Tref, "vap")
                    HRproc_liq = self.c.return_HR_given_VT(self.P, self.T, "liq")
                    HRref_liq = self.c.return_HR_given_VT(self.Pref, self.Tref, "liq")
                    self.deltaH_liq = self.deltaH_IG - (HRproc_liq - HRref_liq)
                    self.deltaH_vap = self.deltaH_IG - (HRproc_vap - HRref_vap)
                    msg = "deltaH [J mol-1]: " + utils.float2str(self.deltaH_liq, 4, lt=_lt,
                                                                 gt=_gt) + " (liq.), " + utils.float2str(
                        self.deltaH_vap, 4, lt=_lt, gt=_gt) + " (vap.)"
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    print("error calculating deltaH")

                # deltaS_IG
                try:
                    self.deltaS_IG = IGprop.return_deltaS_IG(self.Tref, self.T, self.Pref, self.P,
                                                             a0, a1, a2, a3, a4)
                    msg = "deltaS_IG " + " [J mol-1 K-1]: " + utils.float2str(self.deltaS_IG, 4, lt=_lt, gt=_gt)
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    # TODO
                    print("error calculating deltaS_IG")

                # deltaS
                try:
                    SRproc_vap = self.c.return_SR_given_VT(self.P, self.T, "vap")
                    SRref_vap = self.c.return_SR_given_VT(self.Pref, self.Tref, "vap")
                    SRproc_liq = self.c.return_SR_given_VT(self.P, self.T, "liq")
                    SRref_liq = self.c.return_SR_given_VT(self.Pref, self.Tref, "liq")
                    self.deltaS_liq = self.deltaS_IG - (SRproc_liq - SRref_liq)
                    self.deltaS_vap = self.deltaS_IG - (SRproc_vap - SRref_vap)
                    msg = "deltaS [J mol-1 K-1]: " + utils.float2str(self.deltaS_liq, 4, lt=_lt,
                                                                     gt=_gt) + " (liq.), " + utils.float2str(
                        self.deltaS_vap, 4, lt=_lt, gt=_gt) + " (vap.)"
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    # TODO
                    print("error calculating deltaS")

                # deltaG_IG
                try:
                    self.deltaG_IG = IGprop.return_deltaG_IG(self.deltaH_IG, self.T, self.deltaS_IG)
                    msg = "deltaG_IG " + " [J mol-1]: " + utils.float2str(self.deltaG_IG, 4, lt=_lt, gt=_gt)
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    # TODO
                    print("error calculating deltaG_IG")

                # deltaG
                try:
                    GRproc_vap = self.c.return_GR_given_VT(self.P, self.T, "vap")
                    GRref_vap = self.c.return_GR_given_VT(self.Pref, self.Tref, "vap")
                    GRproc_liq = self.c.return_GR_given_VT(self.P, self.T, "liq")
                    GRref_liq = self.c.return_GR_given_VT(self.Pref, self.Tref, "liq")
                    self.deltaG_liq = self.deltaG_IG - (GRproc_liq - GRref_liq)
                    self.deltaG_vap = self.deltaG_IG - (GRproc_vap - GRref_vap)
                    msg = "deltaG [J mol-1 K-1]: " + utils.float2str(self.deltaG_liq, 4, lt=_lt,
                                                                     gt=_gt) + " (liq.), " + utils.float2str(
                        self.deltaG_vap, 4, lt=_lt, gt=_gt) + " (vap.)"
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    # TODO
                    print("error calculating deltaG")

                # deltaU_IG
                try:
                    self.deltaU_IG = IGprop.return_deltaU_IG(self.deltaG_IG, self.T, self.deltaS_IG)
                    msg = "deltaU_IG " + " [J mol-1]: " + utils.float2str(self.deltaU_IG, 4, lt=_lt, gt=_gt)
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    # TODO
                    print("error calculating deltaU_IG")

                # deltaU
                try:
                    URproc_vap = self.c.return_UR_given_VT(self.P, self.T, "vap")
                    URref_vap = self.c.return_UR_given_VT(self.Pref, self.Tref, "vap")
                    URproc_liq = self.c.return_UR_given_VT(self.P, self.T, "liq")
                    URref_liq = self.c.return_UR_given_VT(self.Pref, self.Tref, "liq")
                    self.deltaU_liq = self.deltaU_IG - (URproc_liq - URref_liq)
                    self.deltaU_vap = self.deltaU_IG - (URproc_vap - URref_vap)
                    msg = "deltaU [J mol-1 K-1]: " + utils.float2str(self.deltaU_liq, 4, lt=_lt,
                                                                     gt=_gt) + " (liq.), " + utils.float2str(
                        self.deltaU_vap, 4, lt=_lt, gt=_gt) + " (vap.)"
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    # TODO
                    print("error calculating deltaU")

                # deltaA_IG
                try:
                    self.deltaA_IG = IGprop.return_deltaA_IG(self.deltaU_IG, self.T, self.deltaS_IG)
                    msg = "deltaA_IG " + " [J mol-1]: " + utils.float2str(self.deltaA_IG, 4, lt=_lt, gt=_gt)
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    # TODO
                    print("error calculating deltaA_IG")

                # deltaA
                try:
                    ARproc_vap = self.c.return_AR_given_VT(self.P, self.T, "vap")
                    ARref_vap = self.c.return_AR_given_VT(self.Pref, self.Tref, "vap")
                    ARproc_liq = self.c.return_AR_given_VT(self.P, self.T, "liq")
                    ARref_liq = self.c.return_AR_given_VT(self.Pref, self.Tref, "liq")
                    self.deltaA_liq = self.deltaA_IG - (ARproc_liq - ARref_liq)
                    self.deltaA_vap = self.deltaA_IG - (ARproc_vap - ARref_vap)
                    msg = "deltaA [J mol-1 K-1]: " + utils.float2str(self.deltaA_liq, 4, lt=_lt,
                                                                     gt=_gt) + " (liq.), " + utils.float2str(
                        self.deltaA_vap, 4, lt=_lt, gt=_gt) + " (vap.)"
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    # TODO
                    print("error calculating deltaA")

                # fugacity
                try:
                    self.fugacity_liq = self.c.return_fliq_given_VT(self.P, self.T) * units.Pa_to_bar
                    self.fugacity_vap = self.c.return_fvap_given_VT(self.P, self.T) * units.Pa_to_bar
                    msg = "fugacity [bar]: " + utils.float2str(self.fugacity_liq, 4, lt=_lt,
                                                               gt=_gt) + " (liq.), " + utils.float2str(
                        self.fugacity_vap, 4, lt=_lt, gt=_gt) + " (vap.)"
                    self.plainTextEdit_results.appendPlainText(msg)
                except:
                    # TODO
                    print("error calculating fugacity")

                # Pvp from EOS
                try:
                    tol = 1e-4
                    maxit = 100
                    try:
                        self.Pvp_eos, k = self.c.return_Pvp_EOS(self.T, self.P_antoine, tol=tol, k=maxit)  # Pa
                    except:
                        self.Pvp_eos, k = self.c.return_Pvp_EOS(self.T, units.bar_to_Pa, tol=tol, k=maxit)  # Pa
                    msg = "Pvp (EOS) [bar]: " + utils.float2str(self.Pvp_eos * units.Pa_to_bar, 4,
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
                query = "SELECT * FROM database WHERE Name LIKE '%" + substance_string_name + "%'" + \
                        " OR Formula LIKE '%" + substance_string_name + "%'" + \
                        " OR `CAS #` LIKE '%" + substance_string_name + "%'"
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
