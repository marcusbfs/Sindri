# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/vle_ui.ui',
# licensing of 'designer/vle_ui.ui' applies.
#
# Created: Mon Mar 25 17:45:29 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_FormVLE(object):
    def setupUi(self, FormVLE):
        FormVLE.setObjectName("FormVLE")
        FormVLE.setWindowModality(QtCore.Qt.ApplicationModal)
        FormVLE.resize(750, 485)
        self.gridLayout = QtWidgets.QGridLayout(FormVLE)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(FormVLE)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 730, 465))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_2.addItem(spacerItem, 1, 2, 1, 1)
        self.comboBox_EOS = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_EOS.setObjectName("comboBox_EOS")
        self.gridLayout_2.addWidget(self.comboBox_EOS, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.tabWidget_VLE = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget_VLE.setObjectName("tabWidget_VLE")
        self.tab_VLEcalc = QtWidgets.QWidget()
        self.tab_VLEcalc.setObjectName("tab_VLEcalc")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_VLEcalc)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.groupBox = QtWidgets.QGroupBox(self.tab_VLEcalc)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_VarAnswer = QtWidgets.QLabel(self.groupBox)
        self.label_VarAnswer.setObjectName("label_VarAnswer")
        self.gridLayout_5.addWidget(self.label_VarAnswer, 0, 0, 1, 1)
        self.label_VarAnswerUnits = QtWidgets.QLabel(self.groupBox)
        self.label_VarAnswerUnits.setObjectName("label_VarAnswerUnits")
        self.gridLayout_5.addWidget(self.label_VarAnswerUnits, 0, 2, 1, 1)
        self.le_scalarAnswer = QtWidgets.QLineEdit(self.groupBox)
        self.le_scalarAnswer.setReadOnly(True)
        self.le_scalarAnswer.setObjectName("le_scalarAnswer")
        self.gridLayout_5.addWidget(self.le_scalarAnswer, 0, 1, 1, 1)
        self.tableWidget_Results = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget_Results.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.tableWidget_Results.setObjectName("tableWidget_Results")
        self.tableWidget_Results.setColumnCount(0)
        self.tableWidget_Results.setRowCount(0)
        self.gridLayout_5.addWidget(self.tableWidget_Results, 1, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_5.addItem(spacerItem1, 0, 3, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox, 0, 1, 1, 1)
        self.frame = QtWidgets.QFrame(self.tab_VLEcalc)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)
        self.comboBox_CalcType = QtWidgets.QComboBox(self.frame)
        self.comboBox_CalcType.setObjectName("comboBox_CalcType")
        self.gridLayout_4.addWidget(self.comboBox_CalcType, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 1)
        self.le_Tvalue = QtWidgets.QLineEdit(self.frame)
        self.le_Tvalue.setObjectName("le_Tvalue")
        self.gridLayout_4.addWidget(self.le_Tvalue, 1, 1, 1, 1)
        self.comboBox_Tunit = QtWidgets.QComboBox(self.frame)
        self.comboBox_Tunit.setObjectName("comboBox_Tunit")
        self.gridLayout_4.addWidget(self.comboBox_Tunit, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 2, 0, 1, 1)
        self.le_Pvalue = QtWidgets.QLineEdit(self.frame)
        self.le_Pvalue.setObjectName("le_Pvalue")
        self.gridLayout_4.addWidget(self.le_Pvalue, 2, 1, 1, 1)
        self.comboBox_Punit = QtWidgets.QComboBox(self.frame)
        self.comboBox_Punit.setObjectName("comboBox_Punit")
        self.gridLayout_4.addWidget(self.comboBox_Punit, 2, 2, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget_MolarFractions = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_MolarFractions.setObjectName("tableWidget_MolarFractions")
        self.tableWidget_MolarFractions.setColumnCount(0)
        self.tableWidget_MolarFractions.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidget_MolarFractions, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 3, 0, 1, 3)
        self.btn_calculate = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.btn_calculate.setFont(font)
        self.btn_calculate.setObjectName("btn_calculate")
        self.gridLayout_4.addWidget(self.btn_calculate, 4, 1, 1, 1)
        self.gridLayout_6.addWidget(self.frame, 0, 0, 1, 1)
        self.tabWidget_VLE.addTab(self.tab_VLEcalc, "")
        self.tab_Diagrams = QtWidgets.QWidget()
        self.tab_Diagrams.setObjectName("tab_Diagrams")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_Diagrams)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.frame_2 = QtWidgets.QFrame(self.tab_Diagrams)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.comboBox_diagramType = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_diagramType.setObjectName("comboBox_diagramType")
        self.gridLayout_8.addWidget(self.comboBox_diagramType, 0, 1, 1, 2)
        self.le_varValue = QtWidgets.QLineEdit(self.frame_2)
        self.le_varValue.setObjectName("le_varValue")
        self.gridLayout_8.addWidget(self.le_varValue, 1, 1, 1, 2)
        self.btn_saveToTxtBinaryMixData = QtWidgets.QPushButton(self.frame_2)
        self.btn_saveToTxtBinaryMixData.setObjectName("btn_saveToTxtBinaryMixData")
        self.gridLayout_8.addWidget(self.btn_saveToTxtBinaryMixData, 8, 2, 1, 2)
        self.le_expDataFileName = QtWidgets.QLineEdit(self.frame_2)
        self.le_expDataFileName.setObjectName("le_expDataFileName")
        self.gridLayout_8.addWidget(self.le_expDataFileName, 2, 2, 1, 2)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.gridLayout_8.addWidget(self.label, 0, 0, 1, 1)
        self.label_var = QtWidgets.QLabel(self.frame_2)
        self.label_var.setObjectName("label_var")
        self.gridLayout_8.addWidget(self.label_var, 1, 0, 1, 1)
        self.btn_openExpData = QtWidgets.QPushButton(self.frame_2)
        self.btn_openExpData.setObjectName("btn_openExpData")
        self.gridLayout_8.addWidget(self.btn_openExpData, 2, 0, 1, 2)
        self.comboBox_varUnit = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_varUnit.setObjectName("comboBox_varUnit")
        self.gridLayout_8.addWidget(self.comboBox_varUnit, 1, 3, 1, 1)
        self.btn_plot = QtWidgets.QPushButton(self.frame_2)
        self.btn_plot.setObjectName("btn_plot")
        self.gridLayout_8.addWidget(self.btn_plot, 8, 0, 1, 2)
        self.checkBox_plotExpData = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_plotExpData.setObjectName("checkBox_plotExpData")
        self.gridLayout_8.addWidget(self.checkBox_plotExpData, 4, 0, 1, 3)
        self.checkBox_plotx = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_plotx.setObjectName("checkBox_plotx")
        self.gridLayout_8.addWidget(self.checkBox_plotx, 5, 0, 1, 1)
        self.checkBox_ploty = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_ploty.setObjectName("checkBox_ploty")
        self.gridLayout_8.addWidget(self.checkBox_ploty, 5, 1, 1, 1)
        self.checkBox_plotxy = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_plotxy.setChecked(True)
        self.checkBox_plotxy.setObjectName("checkBox_plotxy")
        self.gridLayout_8.addWidget(self.checkBox_plotxy, 5, 2, 1, 1)
        self.gridLayout_9.addWidget(self.frame_2, 0, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_Diagrams)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.tableWidget_DataResult = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidget_DataResult.setObjectName("tableWidget_DataResult")
        self.tableWidget_DataResult.setColumnCount(0)
        self.tableWidget_DataResult.setRowCount(0)
        self.gridLayout_7.addWidget(self.tableWidget_DataResult, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox_3, 0, 1, 1, 1)
        self.tabWidget_VLE.addTab(self.tab_Diagrams, "")
        self.gridLayout_2.addWidget(self.tabWidget_VLE, 3, 0, 1, 3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(FormVLE)
        self.tabWidget_VLE.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FormVLE)

    def retranslateUi(self, FormVLE):
        FormVLE.setWindowTitle(
            QtWidgets.QApplication.translate(
                "FormVLE", "Vapor-liquid equilibrium", None, -1
            )
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate("FormVLE", "Equation of state", None, -1)
        )
        self.groupBox.setTitle(
            QtWidgets.QApplication.translate("FormVLE", "Results", None, -1)
        )
        self.label_VarAnswer.setText(
            QtWidgets.QApplication.translate("FormVLE", "Var", None, -1)
        )
        self.label_VarAnswerUnits.setText(
            QtWidgets.QApplication.translate("FormVLE", "VarUnits", None, -1)
        )
        self.label_3.setText(
            QtWidgets.QApplication.translate("FormVLE", "Calculation type:", None, -1)
        )
        self.label_4.setText(QtWidgets.QApplication.translate("FormVLE", "T", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("FormVLE", "P", None, -1))
        self.groupBox_2.setTitle(
            QtWidgets.QApplication.translate("FormVLE", "Molar fractions", None, -1)
        )
        self.btn_calculate.setText(
            QtWidgets.QApplication.translate("FormVLE", "Calculate", None, -1)
        )
        self.tabWidget_VLE.setTabText(
            self.tabWidget_VLE.indexOf(self.tab_VLEcalc),
            QtWidgets.QApplication.translate("FormVLE", "VLE calculations", None, -1),
        )
        self.btn_saveToTxtBinaryMixData.setText(
            QtWidgets.QApplication.translate("FormVLE", "Save to txt", None, -1)
        )
        self.label.setText(
            QtWidgets.QApplication.translate("FormVLE", "Type:", None, -1)
        )
        self.label_var.setText(
            QtWidgets.QApplication.translate("FormVLE", "Var", None, -1)
        )
        self.btn_openExpData.setText(
            QtWidgets.QApplication.translate("FormVLE", "Open exp. data", None, -1)
        )
        self.btn_plot.setText(
            QtWidgets.QApplication.translate("FormVLE", "Plot", None, -1)
        )
        self.checkBox_plotExpData.setText(
            QtWidgets.QApplication.translate(
                "FormVLE", "plot experimental data", None, -1
            )
        )
        self.checkBox_plotx.setText(
            QtWidgets.QApplication.translate("FormVLE", "plot x", None, -1)
        )
        self.checkBox_ploty.setText(
            QtWidgets.QApplication.translate("FormVLE", "plot y", None, -1)
        )
        self.checkBox_plotxy.setText(
            QtWidgets.QApplication.translate("FormVLE", "plot xy", None, -1)
        )
        self.groupBox_3.setTitle(
            QtWidgets.QApplication.translate("FormVLE", "Results", None, -1)
        )
        self.tabWidget_VLE.setTabText(
            self.tabWidget_VLE.indexOf(self.tab_Diagrams),
            QtWidgets.QApplication.translate(
                "FormVLE", "Binary mixture diagrams", None, -1
            ),
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    FormVLE = QtWidgets.QWidget()
    ui = Ui_FormVLE()
    ui.setupUi(FormVLE)
    FormVLE.show()
    sys.exit(app.exec_())