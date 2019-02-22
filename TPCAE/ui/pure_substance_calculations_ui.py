# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/pure_substance_calculations_ui.ui',
# licensing of 'designer/pure_substance_calculations_ui.ui' applies.
#
# Created: Fri Feb 22 11:23:23 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_PureSubstanceCalculationsWindow(object):
    def setupUi(self, PureSubstanceCalculationsWindow):
        PureSubstanceCalculationsWindow.setObjectName("PureSubstanceCalculationsWindow")
        PureSubstanceCalculationsWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        PureSubstanceCalculationsWindow.resize(971, 647)
        self.gridLayout_3 = QtWidgets.QGridLayout(PureSubstanceCalculationsWindow)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_resultstxt = QtWidgets.QGroupBox(PureSubstanceCalculationsWindow)
        self.groupBox_resultstxt.setObjectName("groupBox_resultstxt")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_resultstxt)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.plainTextEdit_results = QtWidgets.QPlainTextEdit(self.groupBox_resultstxt)
        self.plainTextEdit_results.setReadOnly(True)
        self.plainTextEdit_results.setPlainText("")
        self.plainTextEdit_results.setObjectName("plainTextEdit_results")
        self.gridLayout_6.addWidget(self.plainTextEdit_results, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_resultstxt, 0, 1, 7, 1)
        self.groupBox_EOS = QtWidgets.QGroupBox(PureSubstanceCalculationsWindow)
        self.groupBox_EOS.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox_EOS.setObjectName("groupBox_EOS")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_EOS)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget_eos_options = QtWidgets.QListWidget(self.groupBox_EOS)
        self.listWidget_eos_options.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.listWidget_eos_options.setAlternatingRowColors(True)
        self.listWidget_eos_options.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.listWidget_eos_options.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget_eos_options.setObjectName("listWidget_eos_options")
        self.gridLayout.addWidget(self.listWidget_eos_options, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_EOS, 1, 0, 1, 1)
        self.groupBox_refVariables = QtWidgets.QGroupBox(
            PureSubstanceCalculationsWindow
        )
        self.groupBox_refVariables.setObjectName("groupBox_refVariables")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_refVariables)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_refVariables)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.le_refT = QtWidgets.QLineEdit(self.groupBox_refVariables)
        self.le_refT.setInputMethodHints(
            QtCore.Qt.ImhDigitsOnly | QtCore.Qt.ImhPreferNumbers
        )
        self.le_refT.setObjectName("le_refT")
        self.horizontalLayout_3.addWidget(self.le_refT)
        self.comboBox_refTunit = QtWidgets.QComboBox(self.groupBox_refVariables)
        self.comboBox_refTunit.setObjectName("comboBox_refTunit")
        self.horizontalLayout_3.addWidget(self.comboBox_refTunit)
        self.gridLayout_7.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_refVariables)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.le_refP = QtWidgets.QLineEdit(self.groupBox_refVariables)
        self.le_refP.setObjectName("le_refP")
        self.horizontalLayout_4.addWidget(self.le_refP)
        self.comboBox_refPunit = QtWidgets.QComboBox(self.groupBox_refVariables)
        self.comboBox_refPunit.setObjectName("comboBox_refPunit")
        self.horizontalLayout_4.addWidget(self.comboBox_refPunit)
        self.gridLayout_7.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_refVariables, 3, 0, 1, 1)
        self.frame = QtWidgets.QFrame(PureSubstanceCalculationsWindow)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_calculate = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_calculate.sizePolicy().hasHeightForWidth()
        )
        self.btn_calculate.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setUnderline(False)
        font.setBold(True)
        self.btn_calculate.setFont(font)
        self.btn_calculate.setObjectName("btn_calculate")
        self.gridLayout_2.addWidget(self.btn_calculate, 0, 0, 1, 1)
        self.btn_diagrams = QtWidgets.QPushButton(self.frame)
        self.btn_diagrams.setObjectName("btn_diagrams")
        self.gridLayout_2.addWidget(self.btn_diagrams, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.frame, 4, 0, 1, 1)
        self.groupBox_processVariables = QtWidgets.QGroupBox(
            PureSubstanceCalculationsWindow
        )
        self.groupBox_processVariables.setMinimumSize(QtCore.QSize(0, 50))
        self.groupBox_processVariables.setObjectName("groupBox_processVariables")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_processVariables)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_processVariables)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.le_procT = QtWidgets.QLineEdit(self.groupBox_processVariables)
        self.le_procT.setInputMethodHints(
            QtCore.Qt.ImhDigitsOnly | QtCore.Qt.ImhPreferNumbers
        )
        self.le_procT.setObjectName("le_procT")
        self.horizontalLayout.addWidget(self.le_procT)
        self.comboBox_procTunit = QtWidgets.QComboBox(self.groupBox_processVariables)
        self.comboBox_procTunit.setObjectName("comboBox_procTunit")
        self.horizontalLayout.addWidget(self.comboBox_procTunit)
        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_processVariables)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.le_procP = QtWidgets.QLineEdit(self.groupBox_processVariables)
        self.le_procP.setObjectName("le_procP")
        self.horizontalLayout_2.addWidget(self.le_procP)
        self.comboBox_procPunit = QtWidgets.QComboBox(self.groupBox_processVariables)
        self.comboBox_procPunit.setObjectName("comboBox_procPunit")
        self.horizontalLayout_2.addWidget(self.comboBox_procPunit)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_processVariables, 2, 0, 1, 1)
        self.groupBox_searchSubstance = QtWidgets.QGroupBox(
            PureSubstanceCalculationsWindow
        )
        self.groupBox_searchSubstance.setObjectName("groupBox_searchSubstance")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_searchSubstance)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btn_searchSubstance = QtWidgets.QPushButton(self.groupBox_searchSubstance)
        self.btn_searchSubstance.setObjectName("btn_searchSubstance")
        self.gridLayout_4.addWidget(self.btn_searchSubstance, 0, 0, 1, 1)
        self.le_searchSubstance = QtWidgets.QLineEdit(self.groupBox_searchSubstance)
        self.le_searchSubstance.setText("")
        self.le_searchSubstance.setObjectName("le_searchSubstance")
        self.gridLayout_4.addWidget(self.le_searchSubstance, 0, 1, 1, 1)
        self.tableWidget_searchSubstance = QtWidgets.QTableWidget(
            self.groupBox_searchSubstance
        )
        self.tableWidget_searchSubstance.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_searchSubstance.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget_searchSubstance.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.tableWidget_searchSubstance.setAlternatingRowColors(True)
        self.tableWidget_searchSubstance.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.tableWidget_searchSubstance.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.tableWidget_searchSubstance.setShowGrid(False)
        self.tableWidget_searchSubstance.setRowCount(0)
        self.tableWidget_searchSubstance.setColumnCount(26)
        self.tableWidget_searchSubstance.setObjectName("tableWidget_searchSubstance")
        self.tableWidget_searchSubstance.setColumnCount(26)
        self.tableWidget_searchSubstance.setRowCount(0)
        self.gridLayout_4.addWidget(self.tableWidget_searchSubstance, 1, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox_searchSubstance, 0, 0, 1, 1)

        self.retranslateUi(PureSubstanceCalculationsWindow)
        QtCore.QObject.connect(
            self.le_searchSubstance,
            QtCore.SIGNAL("returnPressed()"),
            self.btn_searchSubstance.click,
        )
        QtCore.QMetaObject.connectSlotsByName(PureSubstanceCalculationsWindow)
        PureSubstanceCalculationsWindow.setTabOrder(
            self.le_searchSubstance, self.listWidget_eos_options
        )
        PureSubstanceCalculationsWindow.setTabOrder(
            self.listWidget_eos_options, self.le_procT
        )
        PureSubstanceCalculationsWindow.setTabOrder(self.le_procT, self.le_procP)
        PureSubstanceCalculationsWindow.setTabOrder(self.le_procP, self.le_refT)
        PureSubstanceCalculationsWindow.setTabOrder(self.le_refT, self.le_refP)
        PureSubstanceCalculationsWindow.setTabOrder(self.le_refP, self.btn_calculate)
        PureSubstanceCalculationsWindow.setTabOrder(
            self.btn_calculate, self.tableWidget_searchSubstance
        )
        PureSubstanceCalculationsWindow.setTabOrder(
            self.tableWidget_searchSubstance, self.comboBox_procTunit
        )
        PureSubstanceCalculationsWindow.setTabOrder(
            self.comboBox_procTunit, self.plainTextEdit_results
        )
        PureSubstanceCalculationsWindow.setTabOrder(
            self.plainTextEdit_results, self.comboBox_procPunit
        )
        PureSubstanceCalculationsWindow.setTabOrder(
            self.comboBox_procPunit, self.btn_diagrams
        )
        PureSubstanceCalculationsWindow.setTabOrder(
            self.btn_diagrams, self.comboBox_refTunit
        )
        PureSubstanceCalculationsWindow.setTabOrder(
            self.comboBox_refTunit, self.btn_searchSubstance
        )
        PureSubstanceCalculationsWindow.setTabOrder(
            self.btn_searchSubstance, self.comboBox_refPunit
        )

    def retranslateUi(self, PureSubstanceCalculationsWindow):
        PureSubstanceCalculationsWindow.setWindowTitle(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow",
                "Pure Substance Calculations",
                None,
                -1,
            )
        )
        self.groupBox_resultstxt.setTitle(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Results", None, -1
            )
        )
        self.groupBox_EOS.setTitle(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Equation of state", None, -1
            )
        )
        self.groupBox_refVariables.setTitle(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Reference variables", None, -1
            )
        )
        self.label_3.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "T", None, -1
            )
        )
        self.le_refT.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "300", None, -1
            )
        )
        self.label_4.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "P", None, -1
            )
        )
        self.le_refP.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "1", None, -1
            )
        )
        self.btn_calculate.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Calculate", None, -1
            )
        )
        self.btn_diagrams.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Diagrams", None, -1
            )
        )
        self.groupBox_processVariables.setTitle(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Process variables", None, -1
            )
        )
        self.label.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "T", None, -1
            )
        )
        self.le_procT.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "150", None, -1
            )
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "P", None, -1
            )
        )
        self.le_procP.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "1", None, -1
            )
        )
        self.groupBox_searchSubstance.setTitle(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Search substance", None, -1
            )
        )
        self.btn_searchSubstance.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Search", None, -1
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    PureSubstanceCalculationsWindow = QtWidgets.QWidget()
    ui = Ui_PureSubstanceCalculationsWindow()
    ui.setupUi(PureSubstanceCalculationsWindow)
    PureSubstanceCalculationsWindow.show()
    sys.exit(app.exec_())
