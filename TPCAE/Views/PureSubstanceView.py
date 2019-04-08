from PySide2 import QtCore, QtWidgets

import reports
import units
import utils

# from Controllers.PureSubstanceController import PureSubstanceController
from DatabaseInterface.DatabaseTableWidgetView import DatabaseTableWidgetView
from EOSPureSubstanceInterface import EOSPureSubstanceInterface as EOS
from Factories.EOSMixFactory import getEOSMixOptions
from Models.PureSubstanceModel import PureSubstanceModel
from compounds import MixtureProp, SubstanceProp
from pureSubstanceDiagramsWindow import Window_PureSubstanceDiagrams
from ui.pure_substance_calculations_ui import Ui_PureSubstanceCalculationsWindow
from units import conv_unit
from unitsOptionsWindow import Window_UnitsOptions


class PureSubstanceView(QtWidgets.QWidget, Ui_PureSubstanceCalculationsWindow):
    def __init__(
        self,
        # controller: PureSubstanceController,
        controller,
        model: PureSubstanceModel,
        parent=None,
    ):
        super(PureSubstanceView, self).__init__(parent)
        self.setupUi(self)

        self.controller = controller
        self.model = model
        # self.model.registerSubstanceObserver(self)
        # self.model.registerEOSObserver(self)
        self.model.registerCalculationsObserver(self)

        self.btn_calculate.clicked.connect(self.calculatePureSubstance)
        self.btn_diagrams.clicked.connect(self.open_diagrams)
        self.btn_savetxt.clicked.connect(self.save_to_txt)
        self.btn_units.clicked.connect(self.open_units_options)

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

        self.units = self.controller.units

        # Database tablewidget search
        self.databasetablewidget = DatabaseTableWidgetView(
            self.tableWidget_searchSubstance,
            self.le_searchSubstance,
            self.btn_searchSubstance,
        )

        # listview -> eos options
        # self.listWidget_eos_options.addItems(list(eos.eos_options.keys()))
        eosmixoptions = getEOSMixOptions()
        self.groupBox_EOS.setTitle(
            "Equation of state ({:d})".format(int(len(eosmixoptions)))
        )
        self.listWidget_eos_options.addItems(eosmixoptions)
        self.listWidget_eos_options.itemSelectionChanged.connect(self.eos_selected)
        self.tableWidget_searchSubstance.itemSelectionChanged.connect(
            self.substance_selected
        )

    def updateEOS(self):
        self.setWindowTitle(
            "Pure substance calculations - {}".format(self.model.getEOS())
        )

    def updateSubstance(self):
        pass

    def updateCalculations(self):

        self.plainTextEdit_information.clear()
        self.tableWidget_results.setRowCount(0)
        self.plainTextEdit_log.clear()
        self.sname = self.model.getSubstanceName()
        self.sformula = self.model.getSubstanceFormula()
        self.eosname = self.model.getEOS()
        self.T = self.model.getT()
        self.Tref = self.model.getTref()
        self.P = self.model.getP()
        self.Pref = self.model.getPref()

        self.info = ""
        self.info += "Compound: {:s} ({:s})\n".format(self.sname, self.sformula)

        self.info += "Equation of state: {0:s}\n".format(self.eosname)
        self.info += "Process state: {0:.3f} {1:s}, {2:s} {3:s}\n".format(
            conv_unit(self.T, "K", self.units["T"]),
            self.units["T"],
            utils.f2str(conv_unit(self.P, "Pa", self.units["P"]), 3, lt=1e-2, gt=1e4),
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
        self.info += "State: {0:s}".format(self.model.getFluidState())
        self.plainTextEdit_information.appendPlainText(self.info)

        self.propsliq = self.model.getPropsLiq()
        self.propsvap = self.model.getPropsVap()
        self.Pvp = self.model.getPvp()

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
            msg = QtWidgets.QMessageBox.about(self, "Error showing results", str(e))
            return 1

        try:
            self.log = self.model.getLog()
            self.plainTextEdit_log.appendPlainText(self.log)
        except Exception as e:
            print("Couldn't generate report")
            print(str(e))

    @QtCore.Slot()
    def calculatePureSubstance(self):
        self.controller.calculate()

    @QtCore.Slot()
    def open_diagrams(self):
        if len(self.sname.strip()) > 1 and len(self.eosname.strip()) > 1:

            _decimals = 7
            _lt = 1e-3
            _gt = 1e4

            try:  # to initialize EOS
                self.subs = SubstanceProp(self.sname, self.sformula)
                self.mix = MixtureProp([self.subs], [1.0])
                # self.eoseq = EOS(self.mix, [[0]], self.eosname)
                self.eoseq = EOS([self.subs], self.eosname)
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
                self.eoseq, self.Pref, self.Tref
            )
            self.diagramsWindow.show()

        else:
            msg = QtWidgets.QMessageBox.about(
                self, "Error", "Please, select compound and EOS"
            )
            return

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
            name_suggestion = self.sname + ".txt"
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
    def eos_selected(self):
        self.eosname = self.listWidget_eos_options.currentItem().text()
        self.controller.setEOS(self.eosname)

    @QtCore.Slot()
    def substance_selected(self):
        current_row = self.tableWidget_searchSubstance.currentRow()
        if current_row > -1:
            self.sname = self.tableWidget_searchSubstance.item(current_row, 1).text()
            self.sformula = self.tableWidget_searchSubstance.item(current_row, 0).text()
            self.controller.setSubstance(self.sname, self.sformula)
