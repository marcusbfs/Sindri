from PySide2 import QtCore, QtWidgets, QtGui

import reports
import units
from DatabaseInterface.DatabaseTableWidgetView import DatabaseTableWidgetView
from Factories.EOSMixFactory import getEOSMixOptions
from Models.MixtureModel import MixtureModel
from Properties import VaporPressure
from ui.mixture_calculations_ui import Ui_MixtureCalculationWindow


class MixtureCalculationsView(QtWidgets.QWidget, Ui_MixtureCalculationWindow):
    def __init__(self, controller, model: MixtureModel, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/images/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.setWindowIcon(icon)

        self.model = model

        from Controllers.MixtureCalculationsController import (
            MixtureCalculationsController,
        )

        self.controller: MixtureCalculationsController = controller
        self.model.registerCalculationsObserver(self)
        # self.model.registerSubstanceObserver(self)

        # connect
        self.btn_Add.clicked.connect(self.add_substance_to_system)
        self.btn_Remove.clicked.connect(self.remove_substance_from_system)
        self.btn_EditBIParameters.clicked.connect(self.edit_binary_parameters)
        self.btn_units.clicked.connect(self.open_units_options)
        self.btn_calculate.clicked.connect(self.calculateMixProperties)
        self.btn_setEquimolar.clicked.connect(self.clicked_setEquimolar)
        self.btn_savetxt.clicked.connect(self.save_to_txt)
        self.btn_SaveSystem.clicked.connect(self.saveSystem)
        self.btn_LoadSystem.clicked.connect(self.loadSystem)
        self.btn_VLE.clicked.connect(self.openVLEWindow)

        # add combobox units options
        self.comboBox_procTunit.addItems(units.temperature_options)
        self.comboBox_refTunit.addItems(units.temperature_options)
        self.comboBox_procPunit.addItems(units.pressure_options)
        self.comboBox_refPunit.addItems(units.pressure_options)

        self.units = self.controller.units

        self.k = [[0, 0]]
        self.n = 0
        self.y = [0]
        self.subs_in_system = None
        self.mix = None
        self.eos = None
        self.eosname = None

        # validators
        from validators import getDoubleValidatorRegex, getPositiveIntValidator

        doublevalidator = getDoubleValidatorRegex(self)
        self.le_procT.setValidator(doublevalidator)
        self.le_procP.setValidator(doublevalidator)
        self.le_refT.setValidator(doublevalidator)
        self.le_refP.setValidator(doublevalidator)

        # results header
        self.ResultsColumnsLabels = ["Liquid", "Vapor"]
        self.tableWidget_results.setColumnCount(2)
        self.tableWidget_results.setHorizontalHeaderLabels(self.ResultsColumnsLabels)
        h_header = self.tableWidget_results.horizontalHeader()
        h_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        h_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.tableWidget_searchSubstance.horizontalHeader().setDefaultAlignment(
            QtCore.Qt.AlignLeft
        )
        self.tableWidget_results.horizontalHeader().setDefaultAlignment(
            QtCore.Qt.AlignRight
        )

        # Database tablewidget search
        self.databasetablewidget = DatabaseTableWidgetView(
            self.tableWidget_searchSubstance,
            self.le_searchSubstance,
            self.btn_searchSubstance,
        )

        mixeosoptions = getEOSMixOptions()
        self.groupBox_EOS.setTitle(
            "Equation of state ({:d})".format(int(len(mixeosoptions)))
        )
        self.listWidget_eos_options.addItems(mixeosoptions)

    @QtCore.Slot()
    def open_units_options(self):
        self.controller.openUnitsOptionsClicked()

    @QtCore.Slot()
    def add_substance_to_system(self):
        self.controller.addClicked()

    @QtCore.Slot()
    def remove_substance_from_system(self):
        self.controller.removeClicked()

    @QtCore.Slot()
    def calculateMixProperties(self):
        self.controller.calculatePropsClicked()

    @QtCore.Slot()
    def edit_binary_parameters(self):
        self.controller.editBinIntClicked()

    def updateCalculations(self):
        propsliq = self.model.getPropsLiq()
        propsvap = self.model.getPropsVap()
        Pvp = VaporPressure()
        log = propsliq.log

        try:
            rowlabels, liq, vap = reports.tablewidget_vap_liq_reports(
                propsliq, propsvap, Pvp, **self.units
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
            msg = QtWidgets.QMessageBox.about(
                self, "Error showing mixture results", str(e)
            )
            return 1

        try:
            self.plainTextEdit_log.appendPlainText(log)
        except Exception as e:
            print("Couldn't generate report")
            print(str(e))

        report = ""

        def fmt(label, liq, vap):
            return "{:<25}\t{:>20}\t{:>20}\n".format(str(label), str(liq), str(vap))

        report += fmt("Properties", "Liquid", "Vapor")

        for i in range(len(rowlabels)):
            lbl = rowlabels[i]
            l = liq[i]
            v = vap[i]
            report += fmt(str(lbl), str(l), str(v))
        self.controller.setReport(report)

    @QtCore.Slot()
    def clicked_setEquimolar(self):
        self.controller.setEquimolarClicked()

    @QtCore.Slot()
    def save_to_txt(self):
        self.controller.saveToTxtClicked()

    @QtCore.Slot()
    def saveSystem(self):
        self.controller.saveSystemClicked()

    @QtCore.Slot()
    def loadSystem(self):
        self.controller.loadSystemClicked()

    @QtCore.Slot()
    def openVLEWindow(self):
        self.controller.VLEClicked()
