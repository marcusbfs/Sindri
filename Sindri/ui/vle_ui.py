# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/vle_ui.ui',
# licensing of 'designer/vle_ui.ui' applies.
#
# Created: Thu Apr 25 23:14:12 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_FormVLE(object):
    def setupUi(self, FormVLE):
        FormVLE.setObjectName("FormVLE")
        FormVLE.setWindowModality(QtCore.Qt.ApplicationModal)
        FormVLE.resize(770, 420)
        FormVLE.setMinimumSize(QtCore.QSize(770, 300))
        self.gridLayout = QtWidgets.QGridLayout(FormVLE)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(FormVLE)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 750, 400))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget_VLE = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget_VLE.setObjectName("tabWidget_VLE")
        self.tab_VLEcalc = QtWidgets.QWidget()
        self.tab_VLEcalc.setObjectName("tab_VLEcalc")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_VLEcalc)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.groupBox = QtWidgets.QGroupBox(self.tab_VLEcalc)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
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
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_5.addItem(spacerItem, 0, 3, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox, 0, 1, 1, 1)
        self.frame = QtWidgets.QFrame(self.tab_VLEcalc)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.comboBox_CalcType = QtWidgets.QComboBox(self.frame)
        self.comboBox_CalcType.setObjectName("comboBox_CalcType")
        self.gridLayout_4.addWidget(self.comboBox_CalcType, 0, 1, 1, 2)
        self.comboBox_Tunit = QtWidgets.QComboBox(self.frame)
        self.comboBox_Tunit.setObjectName("comboBox_Tunit")
        self.gridLayout_4.addWidget(self.comboBox_Tunit, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 1)
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
        self.le_Tvalue = QtWidgets.QLineEdit(self.frame)
        self.le_Tvalue.setObjectName("le_Tvalue")
        self.gridLayout_4.addWidget(self.le_Tvalue, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)
        self.le_Pvalue = QtWidgets.QLineEdit(self.frame)
        self.le_Pvalue.setObjectName("le_Pvalue")
        self.gridLayout_4.addWidget(self.le_Pvalue, 2, 1, 1, 1)
        self.gridLayout_6.addWidget(self.frame, 0, 0, 1, 1)
        self.tabWidget_VLE.addTab(self.tab_VLEcalc, "")
        self.tab_Diagrams = QtWidgets.QWidget()
        self.tab_Diagrams.setObjectName("tab_Diagrams")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_Diagrams)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_Diagrams)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.tableWidget_DataResult = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidget_DataResult.setObjectName("tableWidget_DataResult")
        self.tableWidget_DataResult.setColumnCount(0)
        self.tableWidget_DataResult.setRowCount(0)
        self.gridLayout_7.addWidget(self.tableWidget_DataResult, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox_3, 0, 1, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.tab_Diagrams)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_diagramType = QtWidgets.QComboBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.comboBox_diagramType.sizePolicy().hasHeightForWidth()
        )
        self.comboBox_diagramType.setSizePolicy(sizePolicy)
        self.comboBox_diagramType.setObjectName("comboBox_diagramType")
        self.horizontalLayout.addWidget(self.comboBox_diagramType)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_var = QtWidgets.QLabel(self.frame_2)
        self.label_var.setObjectName("label_var")
        self.horizontalLayout_2.addWidget(self.label_var)
        self.le_varValue = QtWidgets.QLineEdit(self.frame_2)
        self.le_varValue.setReadOnly(False)
        self.le_varValue.setObjectName("le_varValue")
        self.horizontalLayout_2.addWidget(self.le_varValue)
        self.comboBox_varUnit = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_varUnit.setObjectName("comboBox_varUnit")
        self.horizontalLayout_2.addWidget(self.comboBox_varUnit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_8.addLayout(self.verticalLayout, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_8.addItem(spacerItem2, 3, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.btn_plot = QtWidgets.QPushButton(self.frame_2)
        self.btn_plot.setObjectName("btn_plot")
        self.horizontalLayout_6.addWidget(self.btn_plot)
        self.btn_saveToTxtBinaryMixData = QtWidgets.QPushButton(self.frame_2)
        self.btn_saveToTxtBinaryMixData.setObjectName("btn_saveToTxtBinaryMixData")
        self.horizontalLayout_6.addWidget(self.btn_saveToTxtBinaryMixData)
        self.gridLayout_8.addLayout(self.horizontalLayout_6, 6, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_plotx = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_plotx.setObjectName("checkBox_plotx")
        self.horizontalLayout_5.addWidget(self.checkBox_plotx)
        self.checkBox_ploty = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_ploty.setObjectName("checkBox_ploty")
        self.horizontalLayout_5.addWidget(self.checkBox_ploty)
        self.checkBox_plotxy = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_plotxy.setChecked(True)
        self.checkBox_plotxy.setObjectName("checkBox_plotxy")
        self.horizontalLayout_5.addWidget(self.checkBox_plotxy)
        self.gridLayout_8.addLayout(self.horizontalLayout_5, 4, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_openExpData = QtWidgets.QPushButton(self.frame_2)
        self.btn_openExpData.setObjectName("btn_openExpData")
        self.horizontalLayout_3.addWidget(self.btn_openExpData)
        self.le_expDataFileName = QtWidgets.QLineEdit(self.frame_2)
        self.le_expDataFileName.setReadOnly(True)
        self.le_expDataFileName.setObjectName("le_expDataFileName")
        self.horizontalLayout_3.addWidget(self.le_expDataFileName)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox_plotExpData = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_plotExpData.setObjectName("checkBox_plotExpData")
        self.horizontalLayout_4.addWidget(self.checkBox_plotExpData)
        self.btn_fitKij = QtWidgets.QPushButton(self.frame_2)
        self.btn_fitKij.setObjectName("btn_fitKij")
        self.horizontalLayout_4.addWidget(self.btn_fitKij)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.gridLayout_8.addLayout(self.verticalLayout_2, 2, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_8.addItem(spacerItem4, 1, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_8.addItem(spacerItem5, 5, 0, 1, 1)
        self.gridLayout_9.addWidget(self.frame_2, 0, 0, 1, 1)
        self.tabWidget_VLE.addTab(self.tab_Diagrams, "")
        self.gridLayout_2.addWidget(self.tabWidget_VLE, 3, 0, 1, 6)
        self.comboBox_EOS = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_EOS.setObjectName("comboBox_EOS")
        self.gridLayout_2.addWidget(self.comboBox_EOS, 1, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_2.addItem(spacerItem6, 1, 5, 1, 1)
        self.btn_EditBIParameters = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_EditBIParameters.setObjectName("btn_EditBIParameters")
        self.gridLayout_2.addWidget(self.btn_EditBIParameters, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.checkBox_UNIFAC = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_UNIFAC.setObjectName("checkBox_UNIFAC")
        self.gridLayout_2.addWidget(self.checkBox_UNIFAC, 1, 4, 1, 1)
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
        self.groupBox.setTitle(
            QtWidgets.QApplication.translate("FormVLE", "Results", None, -1)
        )
        self.label_VarAnswer.setText(
            QtWidgets.QApplication.translate("FormVLE", "Var", None, -1)
        )
        self.label_VarAnswerUnits.setText(
            QtWidgets.QApplication.translate("FormVLE", "VarUnits", None, -1)
        )
        self.label_4.setText(QtWidgets.QApplication.translate("FormVLE", "T", None, -1))
        self.groupBox_2.setTitle(
            QtWidgets.QApplication.translate("FormVLE", "Molar fractions", None, -1)
        )
        self.btn_calculate.setText(
            QtWidgets.QApplication.translate("FormVLE", "Calculate", None, -1)
        )
        self.label_5.setText(QtWidgets.QApplication.translate("FormVLE", "P", None, -1))
        self.label_3.setText(
            QtWidgets.QApplication.translate("FormVLE", "Calculation type:", None, -1)
        )
        self.tabWidget_VLE.setTabText(
            self.tabWidget_VLE.indexOf(self.tab_VLEcalc),
            QtWidgets.QApplication.translate("FormVLE", "VLE calculations", None, -1),
        )
        self.groupBox_3.setTitle(
            QtWidgets.QApplication.translate("FormVLE", "Results", None, -1)
        )
        self.label.setText(
            QtWidgets.QApplication.translate("FormVLE", "Type:", None, -1)
        )
        self.label_var.setText(
            QtWidgets.QApplication.translate("FormVLE", "Var", None, -1)
        )
        self.btn_plot.setText(
            QtWidgets.QApplication.translate("FormVLE", "Plot", None, -1)
        )
        self.btn_saveToTxtBinaryMixData.setText(
            QtWidgets.QApplication.translate("FormVLE", "Save to txt", None, -1)
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
        self.btn_openExpData.setText(
            QtWidgets.QApplication.translate("FormVLE", "Open exp. data", None, -1)
        )
        self.checkBox_plotExpData.setText(
            QtWidgets.QApplication.translate(
                "FormVLE", "plot experimental data", None, -1
            )
        )
        self.btn_fitKij.setText(
            QtWidgets.QApplication.translate("FormVLE", "Fit kij", None, -1)
        )
        self.tabWidget_VLE.setTabText(
            self.tabWidget_VLE.indexOf(self.tab_Diagrams),
            QtWidgets.QApplication.translate(
                "FormVLE", "Binary mixture diagrams", None, -1
            ),
        )
        self.btn_EditBIParameters.setText(
            QtWidgets.QApplication.translate(
                "FormVLE", "Edit binary interaction parameters", None, -1
            )
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate("FormVLE", "Equation of state", None, -1)
        )
        self.checkBox_UNIFAC.setText(
            QtWidgets.QApplication.translate("FormVLE", "UNIFAC", None, -1)
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    FormVLE = QtWidgets.QWidget()
    ui = Ui_FormVLE()
    ui.setupUi(FormVLE)
    FormVLE.show()
    sys.exit(app.exec_())
