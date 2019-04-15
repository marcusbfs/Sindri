from PySide2 import QtWidgets, QtGui

from Factories.EOSMixFactory import createEOSMix, getEOSMixOptions
from EOSMixture import calc_options
from ui.vle_ui import Ui_FormVLE
from Models.MixtureModel import MixtureModel
from units import conv_unit, temperature_options, pressure_options

diagram_types = ["isothermal", "isobaric"]


class MixtureVLEView(QtWidgets.QWidget, Ui_FormVLE):
    def __init__(self, controller, model: MixtureModel, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/images/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.setWindowIcon(icon)

        self.model = model
        from Controllers.MixtureVLEController import MixtureVLEController

        self.controller: MixtureVLEController = controller
        # self.controller = controller

        self.molarFractions_headers = ["Name", "Formula", "Molar fraction"]

        self.diagtype = diagram_types[0]
        self.expfilename = ""

        # table widget data result (binary mixture)
        self.tableWidget_DataResult.setColumnCount(3)
        h_header = self.tableWidget_DataResult.horizontalHeader()
        h_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        h_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        h_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        # connections
        self.comboBox_EOS.currentTextChanged.connect(self._setEOSChange)
        self.comboBox_CalcType.currentTextChanged.connect(self._setCalculationChanges)
        self.comboBox_Punit.currentTextChanged.connect(self._setCalculationChanges)
        self.comboBox_Tunit.currentTextChanged.connect(self._setCalculationChanges)
        self.btn_calculate.clicked.connect(self.calculate)
        self.btn_EditBIParameters.clicked.connect(self.editBinParClicked)
        self.comboBox_diagramType.currentTextChanged.connect(self._setDiagType)
        self.btn_openExpData.clicked.connect(self._openExpDataFile)
        self.btn_plot.clicked.connect(self._plot)
        self.btn_fitKij.clicked.connect(self.fitKijClicked)
        self.btn_saveToTxtBinaryMixData.clicked.connect(
            self._saveToTxtBinaryMixtureData
        )

        self.label_VarAnswerUnits.setText("[bar]")

    def calculate(self):
        self.controller.calculateClicked()

    def _setDiagType(self):
        self.controller.setDiagType()

    def _plot(self):
        self.controller.plot()

    def _saveToTxtBinaryMixtureData(self):
        self.controller.saveToTxtBinaryMixtureData()

    def _uncheckX_and_Y(self):
        self.controller._uncheckX_and_Y()

    def _uncheckX_and_XY(self):
        self.controller._uncheckX_and_XY()

    def _uncheckY_and_XY(self):
        self.controller._uncheckY_and_XY()

    def _openExpDataFile(self):
        self.controller.openExpDataFile()

    def _setCalculationChanges(self):
        self.controller.calculationTypeChanged()

    def _connectPlotCheckBox(self):
        self.controller._connectPlotCheckBox()

    def _disconnectPlotCheckBox(self):
        self.controller._disconnectPlotCheckBox()

    def editBinParClicked(self):
        self.controller.editBinParClicked()

    def _setEOSChange(self):
        self.controller.setEOSChange()

    def fitKijClicked(self):
        self.controller.fitKijClicked()
