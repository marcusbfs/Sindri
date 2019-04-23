from PySide2 import QtWidgets

import diagrams
import units
from Controllers.UnitsOptionsController import UnitsOptionsController
from Models.PureSubstanceModel import PureSubstanceModel
from Views.PureSubstanceDiagramsView import PureSubstanceDiagramsView
from Views.PureSubstanceView import PureSubstanceView
from units import conv_unit


class PureSubstanceController:
    def __init__(self, model: PureSubstanceModel):

        self.units = {
            "P": "bar",
            "T": "K",
            "V": "m3/mol",
            "rho": "kg/m3",
            "energy_per_mol": "J/mol",
            "energy_per_mol_temp": "J/molK",
        }
        self._setupDiagramsDict()
        self.data_is_gen = False

        self.model = model
        self.mainView = PureSubstanceView(self, self.model)
        self.unitsOptionsController = UnitsOptionsController()
        self.unitsOptionsController.registerUnitsOptionsObserver(self)

    # getters
    def createUnitsOptionsView(self):
        self.unitsOptionsController.createUnitsOptionsView()

    def createMainView(self):
        self.mainView.show()

    def createDiagramsView(self):
        self.diagramsView = PureSubstanceDiagramsView(self, self.model)
        self.setEOSandSubstance()
        ti, tf = None, None
        if self.model.substance.Tfp:
            ti = self.model.substance.Tfp
        if self.model.substance.Tc:
            tf = self.model.substance.Tc
        self.diagramsView.initialTrange(ti, tf)
        self.diagramsView.comboBox_diagram.clear()
        self.diagramsView.comboBox_TrangeUnit.clear()
        self.diagramsView.comboBox_diagram.addItems(self.getDiagramOptions())
        self.diagramsView.comboBox_TrangeUnit.addItems(units.temperature_options)
        self.diagramsView.update_axis()
        self.diagramsView.le_isotherms.setEnabled(False)
        self.diagramsView.show()

    def getZ(self):
        return self.model.getZ()

    # setters

    def setRef(self, p: float, t: float):
        self.model.setPref(p)
        self.model.setTref(t)

    def setProc(self, p: float, t: float):
        self.model.setP(p)
        self.model.setT(t)

    def setEOS(self, n: str):
        self.model.setEOS(n)

    def setSubstance(self, n: str, f: str):
        self.model.setSubstance(n, f)

    def updateEOS(self):
        print(id(self), "New EOS: {}".format(self.model.getEOS()))

    def calculate(self):

        self.setProcAndRef()
        self.setEOSandSubstance()

        if (
            len(self.model.getSubstanceName().strip()) > 1
            and len(self.model.getEOS().strip()) > 1
        ):
            try:
                self.model.setupSystem()
                self.model.calculate()
            except Exception as e:
                QtWidgets.QMessageBox.about(self.mainView, "Error", str(e))
        else:
            msg = QtWidgets.QMessageBox.about(
                self.mainView, "Error", "Please, select compound and EOS"
            )
            return

    def updateSubstance(self):
        print(
            "New substance: {} ({})".format(
                self.model.getSubstanceName(), self.model.getSubstanceFormula()
            )
        )

    def _setupDiagramsDict(self):

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

    def updateAxisDiagrams(self):

        seldiag_name = self.diagramsView.comboBox_diagram.currentText()
        seldiag = self.diagram_dict[seldiag_name]
        xaxis = self.x_dict[seldiag]
        yaxis = self.y_dict[seldiag]

        self.diagramsView.checkBox_logscale.setChecked(self.logscale[seldiag])
        self.diagramsView.label_xUnits.setText(xaxis + " unit")
        self.diagramsView.label_yUnits.setText(yaxis + " unit")
        self.diagramsView.comboBox_yUnits.clear()
        self.diagramsView.comboBox_xUnits.clear()
        self.diagramsView.comboBox_xUnits.addItems(self.units_options[xaxis])
        self.diagramsView.comboBox_yUnits.addItems(self.units_options[yaxis])

    def genDiagrams(self):

        Tunit = self.diagramsView.comboBox_TrangeUnit.currentText()
        try:
            self.Ti = float(units.conv_unit(self.diagramsView.le_Ti.text(), Tunit, "K"))
            self.Tf = float(units.conv_unit(self.diagramsView.le_Tf.text(), Tunit, "K"))
        except Exception as e:
            print(str(e))
            QtWidgets.QMessageBox.about(
                self.diagramsView, "Error", "T values are not valid numbers"
            )
            return -1
        try:
            self.points = float(self.diagramsView.le_points.text())
        except:
            QtWidgets.QMessageBox.about(
                self.diagramsView, "Error", "Invalid number of points"
            )
            return -1

        try:
            if self.diagramsView.le_isotherms.text() != "":
                self.isotherms_range = [
                    float(i) for i in self.diagramsView.le_isotherms.text().split()
                ]
            else:
                self.isotherms_range = []
        except:
            QtWidgets.QMessageBox.about(
                self.diagramsView, "Error", "Invalid isotherms values"
            )
            return -1

        from time import time

        try:
            s1 = time()
            self.rl, self.rv, self.cp = diagrams.gen_data(
                self.model.system,
                [self.Ti, self.Tf],
                self.model.getPref(),
                self.model.getTref(),
                int(self.points),
                isotherms=self.isotherms_range,
            )
            s2 = time()
            QtWidgets.QMessageBox.information(
                self.diagramsView,
                "Data generated",
                "Computation time: {:.3f} sec".format(s2 - s1),
            )
            self.diag = diagrams.PlotPureSubstanceDiagrams(
                self.rl,
                self.rv,
                self.cp,
                self.model.getSubstanceName(),
                self.model.getEOS(),
            )

        except Exception as e:
            QtWidgets.QMessageBox.about(
                self.diagramsView, "Error generating data", str(e)
            )
            return

        self.data_is_gen = True

    def getDiagramOptions(self):
        return list(self.diagram_dict.keys())

    def plotDiagrams(self):

        if self.data_is_gen:
            xunit = self.diagramsView.comboBox_xUnits.currentText()
            yunit = self.diagramsView.comboBox_yUnits.currentText()
            seldiag_name = self.diagramsView.comboBox_diagram.currentText()
            choice = self.diagram_dict[seldiag_name]
            try:
                if choice == "PV":
                    self.diag.plotPV(
                        xunit,
                        yunit,
                        lnscale=self.diagramsView.checkBox_logscale.isChecked(),
                        grid=self.diagramsView.checkBox_grid.isChecked(),
                        smooth=self.diagramsView.checkBox_smooth.isChecked(),
                    )
                elif choice == "TS":
                    self.diag.plotTS(
                        xunit,
                        yunit,
                        lnscale=self.diagramsView.checkBox_logscale.isChecked(),
                        grid=self.diagramsView.checkBox_grid.isChecked(),
                        smooth=self.diagramsView.checkBox_smooth.isChecked(),
                    )
                elif choice == "PS":
                    self.diag.plotPS(
                        xunit,
                        yunit,
                        lnscale=self.diagramsView.checkBox_logscale.isChecked(),
                        grid=self.diagramsView.checkBox_grid.isChecked(),
                        smooth=self.diagramsView.checkBox_smooth.isChecked(),
                    )
                elif choice == "HS":
                    self.diag.plotHS(
                        xunit,
                        yunit,
                        lnscale=self.diagramsView.checkBox_logscale.isChecked(),
                        grid=self.diagramsView.checkBox_grid.isChecked(),
                        smooth=self.diagramsView.checkBox_smooth.isChecked(),
                    )
                elif choice == "PT":
                    self.diag.plotPT(
                        xunit,
                        yunit,
                        lnscale=self.diagramsView.checkBox_logscale.isChecked(),
                        grid=self.diagramsView.checkBox_grid.isChecked(),
                        smooth=self.diagramsView.checkBox_smooth.isChecked(),
                    )
                elif choice == "TV":
                    self.diag.plotTV(
                        xunit,
                        yunit,
                        lnscale=self.diagramsView.checkBox_logscale.isChecked(),
                        grid=self.diagramsView.checkBox_grid.isChecked(),
                        smooth=self.diagramsView.checkBox_smooth.isChecked(),
                    )
                self.diag._plot()

            except Exception as e:
                print(str(e))
                QtWidgets.QMessageBox.about(
                    self.diagramsView, "Error", "Error plotting curve"
                )
        else:
            QtWidgets.QMessageBox.about(
                self.diagramsView, "Attention", "Please, generate the data first"
            )
            return -1

    def setEOSandSubstance(self):

        eosname = self.mainView.listWidget_eos_options.currentItem().text()
        self.model.setEOS(eosname)

        current_row = self.mainView.tableWidget_searchSubstance.currentRow()
        if current_row > -1:
            sname = self.mainView.tableWidget_searchSubstance.item(
                current_row, 1
            ).text()
            sformula = self.mainView.tableWidget_searchSubstance.item(
                current_row, 0
            ).text()
            self.model.setSubstance(sname, sformula)

    def openDiagramsClicked(self):
        self.setProcAndRef()
        self.setEOSandSubstance()
        self.model.setupSystem()
        self.createDiagramsView()

    def setProcAndRef(self):
        procTunit = self.mainView.comboBox_procTunit.currentText()
        procPunit = self.mainView.comboBox_procPunit.currentText()
        refTunit = self.mainView.comboBox_refTunit.currentText()
        refPunit = self.mainView.comboBox_refPunit.currentText()

        try:
            T = conv_unit(
                float(self.mainView.le_procT.text()), procTunit, "K"
            )  # convert to Kelvin
            P = conv_unit(
                float(self.mainView.le_procP.text()), procPunit, "Pa"
            )  # convert to pascal
            Tref = conv_unit(
                float(self.mainView.le_refT.text()), refTunit, "K"
            )  # convert to Kelvin
            Pref = conv_unit(
                float(self.mainView.le_refP.text()), refPunit, "Pa"
            )  # convert to pascal

            self.model.setPref(Pref)
            self.model.setTref(Tref)
            self.model.setT(T)
            self.model.setP(P)

        except:
            # TODO
            print("error process variables")
            msg = QtWidgets.QMessageBox.about(
                self.mainView, "Error", "Invalid values for T and/or P"
            )
            raise ValueError("Invalid T and/or P numbers")

    def updateUnitsOptions(self):
        self.units = self.unitsOptionsController.units
        self.mainView.units = self.units

    def diagrams_isothermStateChanged(self, state):
        self.diagramsView.le_isotherms.setEnabled(state)
