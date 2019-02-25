from PySide2 import QtCore, QtWidgets
from ui.units_options_ui import Ui_Form_UnitsOptions
import units


class Window_UnitsOptions(QtWidgets.QWidget, Ui_Form_UnitsOptions):

    return_units_dict = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(Window_UnitsOptions, self).__init__(parent)
        self.setupUi(self)

        # connections
        self.btn_ok.clicked.connect(self.ok_pressed)
        self.btn_cancel.clicked.connect(self.cancel_pressed)

        # populate combobox
        self.comboBox_pressure.addItems(units.pressure_options)
        self.comboBox_temperature.addItems(units.temperature_options)
        self.comboBox_volume.addItems(units.molar_vol_options)
        self.comboBox_density.addItems(units.density_options)
        self.comboBox_energ_per_mol.addItems(units.energy_per_mol_options)
        self.comboBox_energ_per_mol_temp.addItems(units.energy_per_mol_temp_options)

    @QtCore.Slot()
    def ok_pressed(self):
        units_dict = {
            "P": self.comboBox_pressure.currentText(),
            "T": self.comboBox_temperature.currentText(),
            "V": self.comboBox_volume.currentText(),
            "rho": self.comboBox_density.currentText(),
            "energy_per_mol": self.comboBox_energ_per_mol.currentText(),
            "energy_per_mol_temp": self.comboBox_energ_per_mol_temp.currentText(),
        }
        self.return_units_dict.emit(units_dict)
        self.close()

    @QtCore.Slot()
    def cancel_pressed(self):
        self.close()
