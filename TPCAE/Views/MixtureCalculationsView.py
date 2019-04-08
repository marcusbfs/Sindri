import numpy as np
from PySide2 import QtCore, QtWidgets

import reports
import units
import utils
from DatabaseInterface.DatabaseTableWidgetView import DatabaseTableWidgetView
from Factories.EOSMixFactory import createEOSMix, getEOSMixOptions
from Properties import VaporPressure
from VLEWindow import Window_VLE
from compounds import MixtureProp, SubstanceProp
from editBinaryInteractionsParametersWin import Window_BinaryInteractionParameters
from ui.mixture_calculations_ui import Ui_MixtureCalculationWindow
from Models.MixtureModel import MixtureModel
from Controllers.UnitsOptionsController import UnitsOptionsController
from units import conv_unit
from unitsOptionsWindow import Window_UnitsOptions


class MixtureCalculationsView(QtWidgets.QWidget, Ui_MixtureCalculationWindow):
    def __init__(self, controller, model: MixtureModel, parent=None):
        super().__init__(parent)
        self.setupUi(self)

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
        # self.btn_Add.clicked.connect(self._changedSystem)
        # self.btn_Remove.clicked.connect(self._changedSystem)
        self.btn_EditBIParameters.clicked.connect(self.edit_binary_parameters)
        self.btn_units.clicked.connect(self.open_units_options)
        self.btn_calculate.clicked.connect(self.calculateMixProperties)
        self.btn_setEquimolar.clicked.connect(self.clicked_setEquimolar)
        # self.btn_savetxt.clicked.connect(self.save_to_txt)
        # self.btn_SaveSystem.clicked.connect(self.saveSystem)
        # self.btn_LoadSystem.clicked.connect(self.loadSystem)
        # self.btn_VLE.clicked.connect(self.openVLEWindow)
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

        self.units = self.controller.units

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
        # self.listWidget_eos_options.itemSelectionChanged.connect(self.eos_selected)

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

    @QtCore.Slot()
    def clicked_setEquimolar(self):
        self.controller.setEquimolarClicked()
