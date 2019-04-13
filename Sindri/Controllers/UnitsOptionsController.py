from Views.UnitsOptionsView import UnitsOptionsView


class UnitsOptionsController:
    def __init__(self):
        self.unitsOptionsObservers = []

        self.units = {
            "P": "bar",
            "T": "K",
            "V": "m3/mol",
            "rho": "kg/m3",
            "energy_per_mol": "J/mol",
            "energy_per_mol_temp": "J/molK",
        }

        self.unitsOptionsView = UnitsOptionsView(self)

    def createUnitsOptionsView(self):
        self.unitsOptionsView.show()

    def okPressedUnitsOptions(self):
        self.units = {
            "P": self.unitsOptionsView.comboBox_pressure.currentText(),
            "T": self.unitsOptionsView.comboBox_temperature.currentText(),
            "V": self.unitsOptionsView.comboBox_volume.currentText(),
            "rho": self.unitsOptionsView.comboBox_density.currentText(),
            "energy_per_mol": self.unitsOptionsView.comboBox_energ_per_mol.currentText(),
            "energy_per_mol_temp": self.unitsOptionsView.comboBox_energ_per_mol_temp.currentText(),
        }
        self.notifyUnitsOptionsObserver()
        self.unitsOptionsView.close()

    def cancePressedUnitsOptions(self):
        self.unitsOptionsView.close()

    def registerUnitsOptionsObserver(self, o):
        self.unitsOptionsObservers.append(o)

    def notifyUnitsOptionsObserver(self):
        for o in self.unitsOptionsObservers:
            o.updateUnitsOptions()
