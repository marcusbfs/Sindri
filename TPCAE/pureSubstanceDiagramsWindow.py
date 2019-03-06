import units
from PySide2 import QtCore, QtWidgets
from ui.pure_substance_diagrams_ui import Ui_Form_PureSubstanceDiagrams
import diagrams
from eos import EOS


class Window_PureSubstanceDiagrams(QtWidgets.QWidget, Ui_Form_PureSubstanceDiagrams):
    def __init__(self, eoseq: EOS, Pref: float, Tref: float , parent=None):
        super(Window_PureSubstanceDiagrams, self).__init__(parent)
        self.setupUi(self)

        self.eoseq = eoseq
        self.Pref = Pref
        self.Tref = Tref

        self.checkBox_smooth.setChecked(True)
        self.checkBox_grid.setChecked(True)
        self.subsname = self.eoseq.mix.substances[0].Name
        self.eos_used = self.eoseq.getEOSDisplayName()

        self.points = 30
        self.data_is_gen = False
        self.le_points.setText(str(self.points))
        # self.le_isotherms.setText("120 150 190")  # TODO remove this line after testing

        # connections
        self.le_Ti.textChanged.connect(self.changed_Trange)
        self.le_points.textChanged.connect(self.changed_Trange)
        self.le_isotherms.textChanged.connect(self.changed_Trange)
        self.btn_gen.clicked.connect(self.gen)
        self.btn_plot.clicked.connect(self.plot)
        self.comboBox_diagram.currentTextChanged.connect(self.update_axis)

        # set initial and final temperatures to freezing and critical point
        if self.eoseq.mix.substances[0].Tfp:
            self.le_Ti.setText(str(self.eoseq.mix.substances[0].Tfp))
        if self.eoseq.mix.substances[0].Tc:
            self.le_Tf.setText(str(self.eoseq.mix.substances[0].Tc))

        # dictionaries
        self.diagram_dict = {
            "pressure-volume": "PV",
            "temperature-entropy": "TS",
            "pressure-entropy": "PS",
            "enthalpy-entropy": "HS",
            "temperature-volume": "TV",
            "pressure-temperature": "PT",
        }
        self.x_dict = {"PV": "V", "TS": "S", "PS": "S", "TV": "V", "PT": "T", "HS": "S"}
        self.y_dict = {"PV": "P", "TS": "T", "PS": "P", "TV": "T", "PT": "P", "HS": "H"}
        self.units_options = {
            "P": units.pressure_options,
            "V": units.molar_vol_options,
            "T": units.temperature_options,
            "S": ["J/molK"],
            "H": units.energy_per_mol_options,
        }
        self.logscale = {
            "PV": True,
            "TS": False,
            "PS": False,
            "TV": True,
            "PT": False,
            "HS": False,
        }

        self.diagram_options = list(self.diagram_dict.keys())

        self.comboBox_diagram.addItems(self.diagram_options)
        self.comboBox_TrangeUnit.addItems(units.temperature_options)

        self.Ti = 0
        self.Tf = 1

        self.update_axis()

    @QtCore.Slot()
    def gen(self):
        Tunit = self.comboBox_TrangeUnit.currentText()
        try:
            self.Ti = float(units.conv_unit(self.le_Ti.text(), Tunit, "K"))
            self.Tf = float(units.conv_unit(self.le_Tf.text(), Tunit, "K"))
        except Exception as e:
            print(str(e))
            QtWidgets.QMessageBox.about(self, "Error", "T values are not valid numbers")
            return -1
        try:
            self.points = float(self.le_points.text())
        except:
            QtWidgets.QMessageBox.about(self, "Error", "Invalid number of points")
            return -1

        try:
            if self.le_isotherms.text() != "":
                self.isotherms_range = [
                    float(i) for i in self.le_isotherms.text().split()
                ]
            else:
                self.isotherms_range = []
        except:
            QtWidgets.QMessageBox.about(self, "Error", "Invalid isotherms values")
            return -1

        from time import time

        try:
            s1 = time()
            self.rl, self. rv, self.cp = diagrams.gen_data(
                self.eoseq,
                [self.Ti, self.Tf],
                self.Pref,
                self.Tref,
                self.points,
                #isotherms=self.isotherms_range,
            )
            s2 = time()
            QtWidgets.QMessageBox.information(
                self, "Data generated", "Computation time: {:.3f} sec".format(s2 - s1)
            )
            self.diag = diagrams.PlotPureSubstanceDiagrams(self.rl, self.rv, self.cp, self.subsname, self.eos_used)

        except Exception as e:
            QtWidgets.QMessageBox.about(self, "Error generating data", str(e))
            return

        self.data_is_gen = True

    @QtCore.Slot()
    def plot(self):
        if self.data_is_gen:
            xunit = self.comboBox_xUnits.currentText()
            yunit = self.comboBox_yUnits.currentText()
            self.choice = self.seldiag
            try:
                if self.choice == "PV":
                    self.diag.plotPV(xunit, yunit, lnscale=self.checkBox_logscale.isChecked(),
                                     grid=self.checkBox_grid.isChecked(), smooth= self.checkBox_smooth.isChecked())
                elif self.choice == "TS":
                    self.diag.plotTS(xunit, yunit, lnscale=self.checkBox_logscale.isChecked(),
                                     grid=self.checkBox_grid.isChecked(), smooth= self.checkBox_smooth.isChecked())
                elif self.choice == "PS":
                    self.diag.plotPS(xunit, yunit, lnscale=self.checkBox_logscale.isChecked(),
                                     grid=self.checkBox_grid.isChecked(), smooth= self.checkBox_smooth.isChecked())
                elif self.choice == "HS":
                    self.diag.plotHS(xunit, yunit, lnscale=self.checkBox_logscale.isChecked(),
                                     grid=self.checkBox_grid.isChecked(), smooth= self.checkBox_smooth.isChecked())
                elif self.choice == "PT":
                    self.diag.plotPT(xunit, yunit, lnscale=self.checkBox_logscale.isChecked(),
                                     grid=self.checkBox_grid.isChecked(), smooth= self.checkBox_smooth.isChecked())
                elif self.choice == "TV":
                    self.diag.plotTV(xunit, yunit, lnscale=self.checkBox_logscale.isChecked(),
                                     grid=self.checkBox_grid.isChecked(), smooth= self.checkBox_smooth.isChecked())
                self.diag._plot()

            except Exception as e:
                print(str(e))
                QtWidgets.QMessageBox.about(self, "Error", "Error plotting curve")
        else:
            QtWidgets.QMessageBox.about(
                self, "Attention", "Please, generate the data first"
            )
            return -1

    @QtCore.Slot()
    def update_axis(self):

        self.seldiag_name = self.comboBox_diagram.currentText()
        self.seldiag = self.diagram_dict[self.seldiag_name]
        self.xaxis = self.x_dict[self.seldiag]
        self.yaxis = self.y_dict[self.seldiag]
        self.checkBox_logscale.setChecked(self.logscale[self.seldiag])
        self.label_xUnits.setText(self.xaxis + " unit")
        self.label_yUnits.setText(self.yaxis + " unit")

        self.comboBox_yUnits.clear()
        self.comboBox_xUnits.clear()
        self.comboBox_xUnits.addItems(self.units_options[self.xaxis])
        self.comboBox_yUnits.addItems(self.units_options[self.yaxis])

    @QtCore.Slot()
    def changed_Trange(self):
        self.data_is_gen = False
