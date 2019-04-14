from PySide2 import QtCore, QtWidgets, QtGui

import units
from ui.units_options_ui import Ui_Form_UnitsOptions


class UnitsOptionsView(QtWidgets.QWidget, Ui_Form_UnitsOptions):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/images/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.setWindowIcon(icon)

        self.controller = controller

        self.units = self.controller.units

        # connections
        self.btn_ok.clicked.connect(self.ok_pressed)
        self.btn_cancel.clicked.connect(self.cancel_pressed)

        # TODO reorder options
        # populate combobox
        self.comboBox_pressure.addItems(units.pressure_options)
        self.comboBox_temperature.addItems(units.temperature_options)
        self.comboBox_volume.addItems(units.molar_vol_options)
        self.comboBox_density.addItems(units.density_options)
        self.comboBox_energ_per_mol.addItems(units.energy_per_mol_options)
        self.comboBox_energ_per_mol_temp.addItems(units.energy_per_mol_temp_options)

        self.comboBox_pressure.setCurrentIndex(
            self.comboBox_pressure.findText(self.units["P"], QtCore.Qt.MatchFixedString)
        )
        self.comboBox_temperature.setCurrentIndex(
            self.comboBox_temperature.findText(
                self.units["T"], QtCore.Qt.MatchFixedString
            )
        )
        self.comboBox_volume.setCurrentIndex(
            self.comboBox_volume.findText(self.units["V"], QtCore.Qt.MatchFixedString)
        )
        self.comboBox_density.setCurrentIndex(
            self.comboBox_density.findText(
                self.units["rho"], QtCore.Qt.MatchFixedString
            )
        )
        self.comboBox_energ_per_mol.setCurrentIndex(
            self.comboBox_energ_per_mol.findText(
                self.units["energy_per_mol"], QtCore.Qt.MatchFixedString
            )
        )
        self.comboBox_energ_per_mol_temp.setCurrentIndex(
            self.comboBox_energ_per_mol_temp.findText(
                self.units["energy_per_mol_temp"], QtCore.Qt.MatchFixedString
            )
        )

    @QtCore.Slot()
    def ok_pressed(self):
        self.controller.okPressedUnitsOptions()

    @QtCore.Slot()
    def cancel_pressed(self):
        self.close()
