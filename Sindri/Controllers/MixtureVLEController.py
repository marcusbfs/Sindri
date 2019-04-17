import numpy as np
from PySide2 import QtWidgets

from Controllers.EditBinaryInteractionParametersController import (
    EditBinaryInteractionParametersController,
)
from Controllers.MixtureCalculationsController import MixtureCalculationsController
from EOSMixture import calc_options
from Factories.EOSMixFactory import getEOSMixOptions
from Models.MixtureModel import MixtureModel
from Views.MixtureVLEView import MixtureVLEView
from units import conv_unit, temperature_options, pressure_options

diagram_types = ["isothermal", "isobaric"]


class MixtureVLEController:
    def __init__(
        self, MixCalcController: MixtureCalculationsController, model: MixtureModel
    ):

        self.model = model
        self.mixCalcController = MixCalcController
        self.vleView: MixtureVLEView = MixtureVLEView(self, self.model)

        self.editBinIntController: EditBinaryInteractionParametersController = EditBinaryInteractionParametersController(
            self.model
        )
        self.n = self.model.getNumberOfSubstancesInSystem()
        self.subsInSystem = self.model.getSubstancesInSystems()
        self.molarFractions_headers = ["Name", "Formula", "Molar fraction"]
        self.calctype = "bubbleP"

    def createMixVLEView(self):
        # initialize tablewidget of molar fractions
        self.vleView.tableWidget_MolarFractions.setRowCount(self.n)
        self.vleView.tableWidget_MolarFractions.setColumnCount(3)

        self.vleView.tableWidget_MolarFractions.setHorizontalHeaderLabels(
            self.vleView.molarFractions_headers
        )
        self.vleView.tableWidget_Results.setRowCount(self.n)
        self.results_col_count = 6
        self.vleView.tableWidget_Results.setColumnCount(self.results_col_count)

        initialMolarFraction = self.mixCalcController.getMolarFractionsFromTable(
            self.mixCalcController.mixtureCalcView.tableWidget_MixtureSystem, 2
        )

        for i in range(self.n):
            n = QtWidgets.QTableWidgetItem(self.subsInSystem[i].Name)
            f = QtWidgets.QTableWidgetItem(self.subsInSystem[i].Formula)
            fraction = QtWidgets.QTableWidgetItem(
                "{:.5f}".format(initialMolarFraction[i])
            )

            self.vleView.tableWidget_MolarFractions.setItem(i, 0, n)
            self.vleView.tableWidget_MolarFractions.setItem(i, 1, f)
            self.vleView.tableWidget_MolarFractions.setItem(i, 2, fraction)
            self.vleView.tableWidget_Results.setItem(
                i, 0, QtWidgets.QTableWidgetItem(self.subsInSystem[i].Name)
            )
            self.vleView.tableWidget_Results.setItem(
                i, 1, QtWidgets.QTableWidgetItem(self.subsInSystem[i].Formula)
            )

        mixeosoptions = getEOSMixOptions()
        # self.comboBox_EOS.addItems(list(vle_options.keys()))
        self.vleView.comboBox_EOS.addItems(mixeosoptions)
        self.vleView.comboBox_CalcType.addItems(list(calc_options.keys()))
        self.vleView.comboBox_Tunit.addItems(temperature_options)
        self.vleView.comboBox_Punit.addItems(pressure_options)

        initialT = str(self.mixCalcController.mixtureCalcView.le_procT.text())
        initialP = str(self.mixCalcController.mixtureCalcView.le_procP.text())
        initialTunit = (
            self.mixCalcController.mixtureCalcView.comboBox_procTunit.currentText()
        )
        initialPunit = (
            self.mixCalcController.mixtureCalcView.comboBox_procPunit.currentText()
        )

        self.vleView.le_Tvalue.setText(initialT)
        self.vleView.le_Pvalue.setText(initialP)
        self.vleView.comboBox_Tunit.setCurrentText(initialTunit)
        self.vleView.comboBox_Punit.setCurrentText(initialPunit)

        if self.n > 2:
            self.vleView.tabWidget_VLE.setTabEnabled(1, False)
        else:
            self.vleView.comboBox_diagramType.addItems(diagram_types)

        self._connectPlotCheckBox()
        self.model.setEOS(
            self.mixCalcController.mixtureCalcView.listWidget_eos_options.currentItem().text()
        )
        self.vleView.comboBox_EOS.setCurrentText(self.model.getEOS())
        self.vleView.show()

    def calculateClicked(self):
        eosname = self.vleView.comboBox_EOS.currentText()
        self.model.setEOS(eosname)

        # check if P and T are numbers
        if not self._PandTareValidNumbers():
            title = "P and T error"
            msg = "P and/or T are not valid numbers"
            QtWidgets.QMessageBox.about(self.vleView, title, msg)
            return -1

        # get molar fractions values
        if not self._areMolarFractonsValidNumbers():
            title = "Molar fraction error"
            msg = "Molar fraction have one or more invalid numbers"
            QtWidgets.QMessageBox.about(self.vleView, title, msg)
            return -1

        p = conv_unit(
            float(self.vleView.le_Pvalue.text()),
            self.vleView.comboBox_Punit.currentText(),
            "Pa",
        )
        t = conv_unit(
            float(self.vleView.le_Tvalue.text()),
            self.vleView.comboBox_Tunit.currentText(),
            "K",
        )

        n = self.model.getNumberOfSubstancesInSystem()
        z = np.empty(n, dtype=np.float64)
        rn = 2
        for i in range(n):
            z[i] = float(self.vleView.tableWidget_MolarFractions.item(i, rn).text())

        if self.calctype == "bubbleP":
            y, p, pv, pl, k, ite = self.model.system.getBubblePointPressure(z, t)
            p = conv_unit(p, "Pa", self.vleView.comboBox_Punit.currentText())
            self.vleView.le_scalarAnswer.setText("{:.5e}".format(p))
            # col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            for i in range(n):
                sy = QtWidgets.QTableWidgetItem("{:.5f}".format(y[i]))
                spv = QtWidgets.QTableWidgetItem("{:.5f}".format(pv[i]))
                spl = QtWidgets.QTableWidgetItem("{:.5f}".format(pl[i]))
                sk = QtWidgets.QTableWidgetItem("{:.5f}".format(k[i]))
                self.vleView.tableWidget_Results.setItem(i, 2, sy)
                self.vleView.tableWidget_Results.setItem(i, 3, spv)
                self.vleView.tableWidget_Results.setItem(i, 4, spl)
                self.vleView.tableWidget_Results.setItem(i, 5, sk)

        elif self.calctype == "dewP":
            x, p, pv, pl, k, ite = self.model.system.getDewPointPressure(z, t)
            p = conv_unit(p, "Pa", self.vleView.comboBox_Punit.currentText())
            self.vleView.le_scalarAnswer.setText("{:.5e}".format(p))
            # col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            for i in range(n):
                sy = QtWidgets.QTableWidgetItem("{:.5f}".format(x[i]))
                spv = QtWidgets.QTableWidgetItem("{:.5f}".format(pv[i]))
                spl = QtWidgets.QTableWidgetItem("{:.5f}".format(pl[i]))
                sk = QtWidgets.QTableWidgetItem("{:.5f}".format(k[i]))
                self.vleView.tableWidget_Results.setItem(i, 2, sy)
                self.vleView.tableWidget_Results.setItem(i, 3, spv)
                self.vleView.tableWidget_Results.setItem(i, 4, spl)
                self.vleView.tableWidget_Results.setItem(i, 5, sk)

        elif self.calctype == "bubbleT":
            y, t, pv, pl, k, ite = self.model.system.getBubblePointTemperature(z, p)
            t = conv_unit(t, "K", self.vleView.comboBox_Tunit.currentText())
            self.vleView.le_scalarAnswer.setText("{:.5e}".format(t))
            # col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            for i in range(n):
                sy = QtWidgets.QTableWidgetItem("{:.5f}".format(y[i]))
                spv = QtWidgets.QTableWidgetItem("{:.5f}".format(pv[i]))
                spl = QtWidgets.QTableWidgetItem("{:.5f}".format(pl[i]))
                sk = QtWidgets.QTableWidgetItem("{:.5f}".format(k[i]))
                self.vleView.tableWidget_Results.setItem(i, 2, sy)
                self.vleView.tableWidget_Results.setItem(i, 3, spv)
                self.vleView.tableWidget_Results.setItem(i, 4, spl)
                self.vleView.tableWidget_Results.setItem(i, 5, sk)

        elif self.calctype == "dewT":
            x, t, pv, pl, k, ite = self.model.system.getDewPointTemperature(z, p)
            t = conv_unit(t, "K", self.vleView.comboBox_Tunit.currentText())
            self.vleView.le_scalarAnswer.setText("{:.5e}".format(t))
            # col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            for i in range(n):
                sy = QtWidgets.QTableWidgetItem("{:.5f}".format(x[i]))
                spv = QtWidgets.QTableWidgetItem("{:.5f}".format(pv[i]))
                spl = QtWidgets.QTableWidgetItem("{:.5f}".format(pl[i]))
                sk = QtWidgets.QTableWidgetItem("{:.5f}".format(k[i]))
                self.vleView.tableWidget_Results.setItem(i, 2, sy)
                self.vleView.tableWidget_Results.setItem(i, 3, spv)
                self.vleView.tableWidget_Results.setItem(i, 4, spl)
                self.vleView.tableWidget_Results.setItem(i, 5, sk)

        else:
            try:
                x, y, v, pv, pl, k, ite = self.model.system.getFlash(z, p, t)
            except Exception as e:
                title = "Error calculating flash"
                msg = str(e)
                QtWidgets.QMessageBox.about(self.vleView, title, msg)
                return -1
            self.vleView.le_scalarAnswer.setText("{:.7f}".format(v))
            col_headers = ["Name", "Formula", "x", "y", "Phivap", "Philiq", "K"]
            for i in range(n):
                sx = QtWidgets.QTableWidgetItem("{:.5f}".format(x[i]))
                sy = QtWidgets.QTableWidgetItem("{:.5f}".format(y[i]))
                spv = QtWidgets.QTableWidgetItem("{:.5f}".format(pv[i]))
                spl = QtWidgets.QTableWidgetItem("{:.5f}".format(pl[i]))
                sk = QtWidgets.QTableWidgetItem("{:.5f}".format(k[i]))
                self.vleView.tableWidget_Results.setItem(i, 2, sx)
                self.vleView.tableWidget_Results.setItem(i, 3, sy)
                self.vleView.tableWidget_Results.setItem(i, 4, spv)
                self.vleView.tableWidget_Results.setItem(i, 5, spl)
                self.vleView.tableWidget_Results.setItem(i, 6, sk)

        tn = self.vleView.tableWidget_Results.columnCount()

        h_header = self.vleView.tableWidget_Results.horizontalHeader()
        for i in range(tn - 2):
            # h_header.setSectionResizeMode(i+2, QtWidgets.QHeaderView.Stretch)
            h_header.setSectionResizeMode(i + 2, QtWidgets.QHeaderView.ResizeToContents)

    def _connectPlotCheckBox(self):
        self.vleView.checkBox_plotx.stateChanged.connect(self.vleView._uncheckY_and_XY)
        self.vleView.checkBox_ploty.stateChanged.connect(self.vleView._uncheckX_and_XY)
        self.vleView.checkBox_plotxy.stateChanged.connect(self.vleView._uncheckX_and_Y)

    def _disconnectPlotCheckBox(self):
        self.vleView.checkBox_plotx.stateChanged.disconnect(
            self.vleView._uncheckY_and_XY
        )
        self.vleView.checkBox_ploty.stateChanged.disconnect(
            self.vleView._uncheckX_and_XY
        )
        self.vleView.checkBox_plotxy.stateChanged.disconnect(
            self.vleView._uncheckX_and_Y
        )

    def _PandTareValidNumbers(self):
        try:
            t = float(self.vleView.le_Tvalue.text()) * 1.0 + 1.0
            p = float(self.vleView.le_Pvalue.text()) * 1.0 + 1.0
            return True
        except:
            return False

    def _areMolarFractonsValidNumbers(self):

        s = 0.0
        n = self.model.getNumberOfSubstancesInSystem()
        try:
            for i in range(n):
                v = float(self.vleView.tableWidget_MolarFractions.item(i, 2).text())
                t = v * 1.0 + 1.0
                s += v
            if abs(s - 1.0) < 1e-6:
                return True
            else:
                return False
        except:
            return False

    def _uncheckX_and_Y(self):
        self._disconnectPlotCheckBox()
        self.vleView.checkBox_plotx.setChecked(False)
        self.vleView.checkBox_ploty.setChecked(False)
        self._connectPlotCheckBox()

    def _uncheckX_and_XY(self):
        self._disconnectPlotCheckBox()
        self.vleView.checkBox_plotx.setChecked(False)
        self.vleView.checkBox_plotxy.setChecked(False)
        self._connectPlotCheckBox()

    def _uncheckY_and_XY(self):
        self._disconnectPlotCheckBox()
        self.vleView.checkBox_plotxy.setChecked(False)
        self.vleView.checkBox_ploty.setChecked(False)
        self._connectPlotCheckBox()

    def calculationTypeChanged(self):
        self.calctype = calc_options[self.vleView.comboBox_CalcType.currentText()]

        for i in range(self.n):
            for j in range(self.results_col_count - 2):
                self.vleView.tableWidget_Results.setItem(
                    i, 2 + j, QtWidgets.QTableWidgetItem("")
                )

        if self.calctype == "bubbleP":
            self.vleView.label_VarAnswer.setText("P")
            varunit = self.vleView.comboBox_Punit.currentText()
            col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            self.vleView.molarFractions_headers[2] = "Liquid molar fractions"

        elif self.calctype == "dewP":
            self.vleView.label_VarAnswer.setText("P")
            varunit = self.vleView.comboBox_Punit.currentText()
            col_headers = ["Name", "Formula", "x", "Phivap", "Philiq", "K"]
            self.vleView.molarFractions_headers[2] = "Vapor molar fractions"
        elif self.calctype == "bubbleT":
            self.vleView.label_VarAnswer.setText("T")
            varunit = self.vleView.comboBox_Tunit.currentText()
            col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            self.vleView.molarFractions_headers[2] = "Liquid molar fractions"

        elif self.calctype == "dewT":
            self.vleView.label_VarAnswer.setText("T")
            varunit = self.vleView.comboBox_Tunit.currentText()
            col_headers = ["Name", "Formula", "x", "Phivap", "Philiq", "K"]
            self.vleView.molarFractions_headers[2] = "Vapor molar fractions"
        else:  # Flash calculation
            self.vleView.label_VarAnswer.setText("Ratio")
            varunit = "-"
            col_headers = ["Name", "Formula", "x", "y", "Phivap", "Philiq", "K"]
            self.vleView.molarFractions_headers[2] = "Feed molar fractions"

        self.vleView.label_VarAnswerUnits.setText("[{}]".format(varunit))

        self.vleView.tableWidget_MolarFractions.setHorizontalHeaderLabels(
            self.molarFractions_headers
        )

        self.results_col_count = len(col_headers)
        self.vleView.tableWidget_Results.setColumnCount(self.results_col_count)
        self.vleView.tableWidget_Results.setHorizontalHeaderLabels(col_headers)

    def editBinParClicked(self):
        self.editBinIntController.createBinInteractionView()

    def setDiagType(self):
        diagtype = self.vleView.comboBox_diagramType.currentText()
        self.vleView.comboBox_varUnit.clear()

        if diagtype == diagram_types[0]:  # isothermal
            self.vleView.label_var.setText("T")
            self.vleView.comboBox_varUnit.addItems(temperature_options)
        else:
            self.vleView.label_var.setText("P")
            self.vleView.comboBox_varUnit.addItems(pressure_options)

    def openExpDataFile(self):

        filename = QtWidgets.QFileDialog.getOpenFileName(self.vleView, "Load file", "")[
            0
        ]

        if not filename:
            return 0

        expfilename = filename
        self.vleView.le_expDataFileName.setText(expfilename)
        self.vleView.checkBox_plotExpData.setChecked(True)

    def plot(self):

        if not self._isGenDataVarValid():
            title = "Variable not valid"
            msg = "Variable is not a valid number"
            QtWidgets.QMessageBox.about(self.vleView, title, msg)
            return -1

        # gendata_header = ["{} [{}]", "x1", "y1"]
        gendata_header = ["{} [{}]", "x1", "y1", "K", "Phi_liq", "Phi_vap"]

        try:
            diagtype = self.vleView.comboBox_diagramType.currentText()
            if diagtype == diagram_types[0]:  # isothermal
                _v = conv_unit(
                    float(self.vleView.le_varValue.text()),
                    self.vleView.comboBox_varUnit.currentText(),
                    "K",
                )
                x, y, var, phiv, phil, kvec = self.model.system.isothermalBinaryMixtureGenData(
                    _v,
                    Tunit=self.vleView.comboBox_varUnit.currentText(),
                    Punit=self.vleView.comboBox_Punit.currentText(),
                )
                gendata_header[0] = "{} [{}]".format(
                    "P", self.vleView.comboBox_Punit.currentText()
                )
            else:
                _v = conv_unit(
                    float(self.vleView.le_varValue.text()),
                    self.vleView.comboBox_varUnit.currentText(),
                    "Pa",
                )
                x, y, var, phiv, phil, kvec = self.model.system.isobaricBinaryMixtureGenData(
                    _v,
                    Tunit=self.vleView.comboBox_Tunit.currentText(),
                    Punit=self.vleView.comboBox_varUnit.currentText(),
                )
                gendata_header[0] = "{} [{}]".format(
                    "T", self.vleView.comboBox_Tunit.currentText()
                )
        except Exception as e:
            title = "Error generating data to plot"
            msg = str(e)
            QtWidgets.QMessageBox.about(self.vleView, title, msg)
            return -1

        # populate table
        n = len(x)
        self.vleView.tableWidget_DataResult.setRowCount(n)
        self.vleView.tableWidget_DataResult.setColumnCount(6)
        self.vleView.tableWidget_DataResult.setHorizontalHeaderLabels(gendata_header)

        for i in range(n):
            item_var = QtWidgets.QTableWidgetItem("{:3.5e}".format(var[i]))
            item_x = QtWidgets.QTableWidgetItem("{:0.5f}".format(x[i]))
            item_y = QtWidgets.QTableWidgetItem("{:0.5f}".format(y[i]))
            item_kvec = QtWidgets.QTableWidgetItem("{:0.5f}".format(kvec[i]))
            item_philiq = QtWidgets.QTableWidgetItem("{:0.5f}".format(phil[i]))
            item_phivap = QtWidgets.QTableWidgetItem("{:0.5f}".format(phiv[i]))

            self.vleView.tableWidget_DataResult.setItem(i, 0, item_var)
            self.vleView.tableWidget_DataResult.setItem(i, 1, item_x)
            self.vleView.tableWidget_DataResult.setItem(i, 2, item_y)
            self.vleView.tableWidget_DataResult.setItem(i, 3, item_kvec)
            self.vleView.tableWidget_DataResult.setItem(i, 4, item_philiq)
            self.vleView.tableWidget_DataResult.setItem(i, 5, item_phivap)

        if self.vleView.checkBox_plotExpData.isChecked():
            expfilename = self.vleView.le_expDataFileName.text()
        else:
            expfilename = ""

        if self.vleView.checkBox_plotx.isChecked():
            plottype = "x"
        elif self.vleView.checkBox_ploty.isChecked():
            plottype = "y"
        else:
            plottype = "both"

        try:

            if diagtype == diagram_types[0]:  # isothermal
                self.model.system.isothermalBinaryMixturePlot(
                    _v,
                    Tunit=self.vleView.comboBox_varUnit.currentText(),
                    Punit=self.vleView.comboBox_Punit.currentText(),
                    expfilename=expfilename,
                    plottype=plottype,
                )
            else:
                self.model.system.isobaricBinaryMixturePlot(
                    _v,
                    Tunit=self.vleView.comboBox_Tunit.currentText(),
                    Punit=self.vleView.comboBox_varUnit.currentText(),
                    expfilename=expfilename,
                    plottype=plottype,
                )
        except Exception as e:
            title = "Error plotting"
            msg = str(e)
            QtWidgets.QMessageBox.about(self.vleView, title, msg)
            return -1

    def _isGenDataVarValid(self):
        try:
            v = float(self.vleView.le_varValue.text()) * 1.0 + 1.0
            return True
        except:
            return False

    def saveToTxtBinaryMixtureData(self):

        try:
            extension = ".txt"
            subs1 = self.subsInSystem[0].Name
            subs2 = self.subsInSystem[1].Name
            var = float(self.vleView.le_varValue.text())
            varunit = self.vleView.comboBox_varUnit.currentText()
            name_suggestion = "{}-{}_at_{:.5f}_{}{}".format(
                subs1, subs2, var, varunit, extension
            )
            txt_file_name = QtWidgets.QFileDialog.getSaveFileName(
                self.vleView,
                "Save binary mixture data",
                name_suggestion,
                "Files (*{})".format(extension),
            )[0]
            if not txt_file_name:
                return 0

        except Exception as e:
            title = "Error getting filename"
            msg = str(e)
            QtWidgets.QMessageBox.about(self.vleView, title, msg)
            return -1

        try:
            i_n = self.vleView.tableWidget_DataResult.rowCount()
            j_n = self.vleView.tableWidget_DataResult.columnCount()

            content = ""

            # header
            diagtype = self.vleView.comboBox_diagramType.currentText()
            if diagtype == diagram_types[0]:
                content += "{}\t".format(self.vleView.comboBox_Punit.currentText())
            else:
                content += "{}\t".format(self.vleView.comboBox_Tunit.currentText())
            content += "{}\t{}\n".format("x1", "y1")

            # data
            for i in range(i_n):
                content += "{}\t{}\t{}\n".format(
                    self.vleView.tableWidget_DataResult.item(i, 0).text(),
                    self.vleView.tableWidget_DataResult.item(i, 1).text(),
                    self.vleView.tableWidget_DataResult.item(i, 2).text(),
                )

            with open(txt_file_name, "w") as file:
                file.write(content)

            title = "Successfully"
            msg = "The file has been saved"
            QtWidgets.QMessageBox.about(self.vleView, title, msg)

        except Exception as e:
            title = "Error saving data to file"
            msg = str(e)
            QtWidgets.QMessageBox.about(self.vleView, title, msg)
            return -1

    def setEOSChange(self):
        self.model.setEOS(self.vleView.comboBox_EOS.currentText())

    def fitKijClicked(self):

        expfilename = self.vleView.le_expDataFileName.text()

        if expfilename == "":
            QtWidgets.QMessageBox.about(self.vleView, "Error", "No experimental data")
            return

        import shlex

        with open(expfilename, "r") as file:
            try:
                content = [line.rstrip("\n") for line in file if line != "\n"]
                n_exp = len(content) - 1
                var_exp = np.empty(n_exp, dtype=np.float64)
                x_exp = np.empty(n_exp, dtype=np.float64)
                y_exp = np.empty(n_exp, dtype=np.float64)
                var_exp_unit = shlex.split(content[0])[0]

                if var_exp_unit in pressure_options:
                    diagtype = "isothermal"
                    varunit = "Pa"
                elif var_exp_unit in temperature_options:
                    diagtype = "isobaric"
                    varunit = "K"
                else:
                    raise ValueError("Diagram type neither 'isothermal' or 'isobaric'")

                for i in range(n_exp):
                    ret3 = shlex.split(content[1 + i])
                    var_exp[i] = conv_unit(float(ret3[0]), var_exp_unit, varunit)
                    x_exp[i] = float(ret3[1])
                    y_exp[i] = float(ret3[2])

            except Exception as e:
                raise ValueError("Error in experimental data\n" + str(e))

        if diagtype == "isothermal":
            conv_isovar_to = "K"
        else:
            conv_isovar_to = "Pa"

        isovar = conv_unit(
            float(self.vleView.le_varValue.text()),
            self.vleView.comboBox_varUnit.currentText(),
            conv_isovar_to,
        )

        from Models.FitExpDataToBinaryParameterModel import (
            FitExpDataToBinaryParameterModel,
        )

        original_k = self.model.getBinaryInteractionsParameters()

        fitExpModel = FitExpDataToBinaryParameterModel(
            self.model, isovar, diagtype, x_exp, y_exp, var_exp
        )
        # WARNING! This method overrides "k" matrix in the model.
        kval = fitExpModel.fitBinaryInteractionParameter()

        self.model.setBinaryInteractionsParameters(original_k)

        self.editBinIntController.createBinInteractionView()
        # self.editBinIntController.binInteractionView.tableWidget_BinaryParameters.setItem(
        #     0, 1, QtWidgets.QTableWidgetItem(str(kval))
        # )
        self.editBinIntController.binInteractionView.tableWidget_BinaryParameters.cellWidget(
            0, 1
        ).setText(
            "{:.7f}".format(kval)
        )
        self.editBinIntController.setSymmetricClicked()
