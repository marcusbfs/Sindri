# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/pure_substance_calculations_ui.ui',
# licensing of 'designer/pure_substance_calculations_ui.ui' applies.
#
# Created: Sun Jun  2 16:59:00 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_PureSubstanceCalculationsWindow(object):
    def setupUi(self, PureSubstanceCalculationsWindow):
        PureSubstanceCalculationsWindow.setObjectName("PureSubstanceCalculationsWindow")
        PureSubstanceCalculationsWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        PureSubstanceCalculationsWindow.resize(900, 740)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            PureSubstanceCalculationsWindow.sizePolicy().hasHeightForWidth()
        )
        PureSubstanceCalculationsWindow.setSizePolicy(sizePolicy)
        PureSubstanceCalculationsWindow.setMinimumSize(QtCore.QSize(900, 300))
        self.gridLayout_9 = QtWidgets.QGridLayout(PureSubstanceCalculationsWindow)
        self.gridLayout_9.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.scrollArea = QtWidgets.QScrollArea(PureSubstanceCalculationsWindow)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 882, 722))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.frame_results = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_results.sizePolicy().hasHeightForWidth()
        )
        self.frame_results.setSizePolicy(sizePolicy)
        self.frame_results.setMinimumSize(QtCore.QSize(300, 0))
        self.frame_results.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_results.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_results.setObjectName("frame_results")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_results)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_information = QtWidgets.QGroupBox(self.frame_results)
        self.groupBox_information.setMinimumSize(QtCore.QSize(0, 115))
        self.groupBox_information.setMaximumSize(QtCore.QSize(16777215, 250))
        self.groupBox_information.setObjectName("groupBox_information")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_information)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.plainTextEdit_information = QtWidgets.QPlainTextEdit(
            self.groupBox_information
        )
        self.plainTextEdit_information.setMinimumSize(QtCore.QSize(0, 0))
        self.plainTextEdit_information.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.plainTextEdit_information.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plainTextEdit_information.setReadOnly(True)
        self.plainTextEdit_information.setObjectName("plainTextEdit_information")
        self.gridLayout_6.addWidget(self.plainTextEdit_information, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_information)
        self.groupBox_results = QtWidgets.QGroupBox(self.frame_results)
        self.groupBox_results.setMinimumSize(QtCore.QSize(0, 350))
        self.groupBox_results.setObjectName("groupBox_results")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_results)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.tableWidget_results = QtWidgets.QTableWidget(self.groupBox_results)
        self.tableWidget_results.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded
        )
        self.tableWidget_results.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.tableWidget_results.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.tableWidget_results.setAlternatingRowColors(False)
        self.tableWidget_results.setTextElideMode(QtCore.Qt.ElideLeft)
        self.tableWidget_results.setRowCount(0)
        self.tableWidget_results.setColumnCount(0)
        self.tableWidget_results.setObjectName("tableWidget_results")
        self.tableWidget_results.setColumnCount(0)
        self.tableWidget_results.setRowCount(0)
        self.tableWidget_results.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget_results.horizontalHeader().setDefaultSectionSize(35)
        self.tableWidget_results.horizontalHeader().setMinimumSectionSize(0)
        self.tableWidget_results.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget_results.verticalHeader().setDefaultSectionSize(21)
        self.tableWidget_results.verticalHeader().setMinimumSectionSize(0)
        self.gridLayout_8.addWidget(self.tableWidget_results, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_results)
        self.groupBox__log = QtWidgets.QGroupBox(self.frame_results)
        self.groupBox__log.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox__log.setMaximumSize(QtCore.QSize(16777215, 250))
        self.groupBox__log.setObjectName("groupBox__log")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox__log)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.plainTextEdit_log = QtWidgets.QPlainTextEdit(self.groupBox__log)
        self.plainTextEdit_log.setMaximumSize(QtCore.QSize(16777215, 166777))
        self.plainTextEdit_log.setReadOnly(True)
        self.plainTextEdit_log.setObjectName("plainTextEdit_log")
        self.gridLayout_3.addWidget(self.plainTextEdit_log, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox__log)
        self.gridLayout_10.addWidget(self.frame_results, 0, 1, 3, 1)
        self.frame_input = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_input.sizePolicy().hasHeightForWidth())
        self.frame_input.setSizePolicy(sizePolicy)
        self.frame_input.setMinimumSize(QtCore.QSize(350, 0))
        self.frame_input.setMaximumSize(QtCore.QSize(1677700, 16777215))
        self.frame_input.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_input.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_input.setObjectName("frame_input")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.frame_input)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.groupBox_searchSubstance = QtWidgets.QGroupBox(self.frame_input)
        self.groupBox_searchSubstance.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox_searchSubstance.setMaximumSize(QtCore.QSize(167772, 16777215))
        self.groupBox_searchSubstance.setObjectName("groupBox_searchSubstance")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_searchSubstance)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btn_searchSubstance = QtWidgets.QPushButton(self.groupBox_searchSubstance)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_searchSubstance.sizePolicy().hasHeightForWidth()
        )
        self.btn_searchSubstance.setSizePolicy(sizePolicy)
        self.btn_searchSubstance.setObjectName("btn_searchSubstance")
        self.gridLayout_4.addWidget(self.btn_searchSubstance, 0, 0, 1, 1)
        self.le_searchSubstance = QtWidgets.QLineEdit(self.groupBox_searchSubstance)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.le_searchSubstance.sizePolicy().hasHeightForWidth()
        )
        self.le_searchSubstance.setSizePolicy(sizePolicy)
        self.le_searchSubstance.setText("")
        self.le_searchSubstance.setObjectName("le_searchSubstance")
        self.gridLayout_4.addWidget(self.le_searchSubstance, 0, 1, 1, 1)
        self.tableWidget_searchSubstance = QtWidgets.QTableWidget(
            self.groupBox_searchSubstance
        )
        self.tableWidget_searchSubstance.setMinimumSize(QtCore.QSize(400, 150))
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
        self.gridLayout_4.addWidget(self.tableWidget_searchSubstance, 2, 0, 1, 2)
        self.gridLayout_11.addWidget(self.groupBox_searchSubstance, 0, 0, 1, 1)
        self.groupBox_EOS = QtWidgets.QGroupBox(self.frame_input)
        self.groupBox_EOS.setMinimumSize(QtCore.QSize(0, 100))
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
        self.gridLayout_11.addWidget(self.groupBox_EOS, 1, 0, 1, 1)
        self.groupBox_processVariables = QtWidgets.QGroupBox(self.frame_input)
        self.groupBox_processVariables.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_processVariables.setMaximumSize(QtCore.QSize(16777215, 55))
        self.groupBox_processVariables.setObjectName("groupBox_processVariables")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_processVariables)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label = QtWidgets.QLabel(self.groupBox_processVariables)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)
        self.le_procT = QtWidgets.QLineEdit(self.groupBox_processVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_procT.sizePolicy().hasHeightForWidth())
        self.le_procT.setSizePolicy(sizePolicy)
        self.le_procT.setInputMethodHints(
            QtCore.Qt.ImhDigitsOnly | QtCore.Qt.ImhPreferNumbers
        )
        self.le_procT.setObjectName("le_procT")
        self.gridLayout_5.addWidget(self.le_procT, 0, 1, 1, 1)
        self.comboBox_procTunit = QtWidgets.QComboBox(self.groupBox_processVariables)
        self.comboBox_procTunit.setObjectName("comboBox_procTunit")
        self.gridLayout_5.addWidget(self.comboBox_procTunit, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_processVariables)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 0, 3, 1, 1)
        self.le_procP = QtWidgets.QLineEdit(self.groupBox_processVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_procP.sizePolicy().hasHeightForWidth())
        self.le_procP.setSizePolicy(sizePolicy)
        self.le_procP.setObjectName("le_procP")
        self.gridLayout_5.addWidget(self.le_procP, 0, 4, 1, 1)
        self.comboBox_procPunit = QtWidgets.QComboBox(self.groupBox_processVariables)
        self.comboBox_procPunit.setObjectName("comboBox_procPunit")
        self.gridLayout_5.addWidget(self.comboBox_procPunit, 0, 5, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_processVariables, 2, 0, 1, 1)
        self.groupBox_refVariables = QtWidgets.QGroupBox(self.frame_input)
        self.groupBox_refVariables.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_refVariables.setMaximumSize(QtCore.QSize(16777215, 55))
        self.groupBox_refVariables.setObjectName("groupBox_refVariables")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_refVariables)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_3 = QtWidgets.QLabel(self.groupBox_refVariables)
        self.label_3.setObjectName("label_3")
        self.gridLayout_7.addWidget(self.label_3, 0, 0, 1, 1)
        self.le_refT = QtWidgets.QLineEdit(self.groupBox_refVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_refT.sizePolicy().hasHeightForWidth())
        self.le_refT.setSizePolicy(sizePolicy)
        self.le_refT.setInputMethodHints(
            QtCore.Qt.ImhDigitsOnly | QtCore.Qt.ImhPreferNumbers
        )
        self.le_refT.setObjectName("le_refT")
        self.gridLayout_7.addWidget(self.le_refT, 0, 1, 1, 1)
        self.comboBox_refTunit = QtWidgets.QComboBox(self.groupBox_refVariables)
        self.comboBox_refTunit.setObjectName("comboBox_refTunit")
        self.gridLayout_7.addWidget(self.comboBox_refTunit, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_refVariables)
        self.label_4.setObjectName("label_4")
        self.gridLayout_7.addWidget(self.label_4, 0, 3, 1, 1)
        self.le_refP = QtWidgets.QLineEdit(self.groupBox_refVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_refP.sizePolicy().hasHeightForWidth())
        self.le_refP.setSizePolicy(sizePolicy)
        self.le_refP.setObjectName("le_refP")
        self.gridLayout_7.addWidget(self.le_refP, 0, 4, 1, 1)
        self.comboBox_refPunit = QtWidgets.QComboBox(self.groupBox_refVariables)
        self.comboBox_refPunit.setObjectName("comboBox_refPunit")
        self.gridLayout_7.addWidget(self.comboBox_refPunit, 0, 5, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_refVariables, 3, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.frame_input)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_units = QtWidgets.QPushButton(self.frame)
        self.btn_units.setObjectName("btn_units")
        self.gridLayout_2.addWidget(self.btn_units, 2, 1, 1, 1)
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
        self.gridLayout_2.addWidget(self.btn_calculate, 2, 0, 1, 1)
        self.btn_diagrams = QtWidgets.QPushButton(self.frame)
        self.btn_diagrams.setObjectName("btn_diagrams")
        self.gridLayout_2.addWidget(self.btn_diagrams, 3, 0, 1, 1)
        self.btn_savetxt = QtWidgets.QPushButton(self.frame)
        self.btn_savetxt.setObjectName("btn_savetxt")
        self.gridLayout_2.addWidget(self.btn_savetxt, 3, 1, 1, 1)
        self.gridLayout_11.addWidget(self.frame, 4, 0, 1, 1)
        self.gridLayout_10.addWidget(self.frame_input, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_9.addWidget(self.scrollArea, 0, 1, 1, 1)

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
        PureSubstanceCalculationsWindow.setTabOrder(
            self.le_refP, self.tableWidget_searchSubstance
        )
        PureSubstanceCalculationsWindow.setTabOrder(
            self.tableWidget_searchSubstance, self.comboBox_procTunit
        )
        PureSubstanceCalculationsWindow.setTabOrder(
            self.comboBox_procTunit, self.comboBox_procPunit
        )
        PureSubstanceCalculationsWindow.setTabOrder(
            self.comboBox_procPunit, self.comboBox_refTunit
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
        self.groupBox_information.setTitle(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Information", None, -1
            )
        )
        self.groupBox_results.setTitle(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Results", None, -1
            )
        )
        self.groupBox__log.setTitle(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Log", None, -1
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
        self.groupBox_EOS.setTitle(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Equation of state", None, -1
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
        self.btn_units.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Units", None, -1
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
        self.btn_savetxt.setText(
            QtWidgets.QApplication.translate(
                "PureSubstanceCalculationsWindow", "Save to txt", None, -1
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
