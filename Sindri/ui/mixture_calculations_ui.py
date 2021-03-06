# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/mixture_calculations_ui.ui',
# licensing of 'designer/mixture_calculations_ui.ui' applies.
#
# Created: Fri Aug 30 18:26:17 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MixtureCalculationWindow(object):
    def setupUi(self, MixtureCalculationWindow):
        MixtureCalculationWindow.setObjectName("MixtureCalculationWindow")
        MixtureCalculationWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MixtureCalculationWindow.resize(770, 635)
        MixtureCalculationWindow.setMinimumSize(QtCore.QSize(770, 0))
        self.gridLayout = QtWidgets.QGridLayout(MixtureCalculationWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(MixtureCalculationWindow)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 750, 615))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_VLE = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_VLE.setObjectName("btn_VLE")
        self.gridLayout_2.addWidget(self.btn_VLE, 1, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName("tabWidget")
        self.tabSystem = QtWidgets.QWidget()
        self.tabSystem.setObjectName("tabSystem")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tabSystem)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame = QtWidgets.QFrame(self.tabSystem)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tableWidget_MixtureSystem = QtWidgets.QTableWidget(self.frame)
        self.tableWidget_MixtureSystem.setMinimumSize(QtCore.QSize(400, 150))
        self.tableWidget_MixtureSystem.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_MixtureSystem.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget_MixtureSystem.setAlternatingRowColors(True)
        self.tableWidget_MixtureSystem.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.tableWidget_MixtureSystem.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectItems
        )
        self.tableWidget_MixtureSystem.setShowGrid(False)
        self.tableWidget_MixtureSystem.setRowCount(0)
        self.tableWidget_MixtureSystem.setColumnCount(3)
        self.tableWidget_MixtureSystem.setObjectName("tableWidget_MixtureSystem")
        self.tableWidget_MixtureSystem.setColumnCount(3)
        self.tableWidget_MixtureSystem.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_MixtureSystem.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_MixtureSystem.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_MixtureSystem.setHorizontalHeaderItem(2, item)
        self.gridLayout_4.addWidget(self.tableWidget_MixtureSystem, 0, 0, 1, 4)
        self.btn_setEquimolar = QtWidgets.QPushButton(self.frame)
        self.btn_setEquimolar.setObjectName("btn_setEquimolar")
        self.gridLayout_4.addWidget(self.btn_setEquimolar, 2, 0, 1, 1)
        self.btn_LoadSystem = QtWidgets.QPushButton(self.frame)
        self.btn_LoadSystem.setMaximumSize(QtCore.QSize(16666000, 16777215))
        self.btn_LoadSystem.setObjectName("btn_LoadSystem")
        self.gridLayout_4.addWidget(self.btn_LoadSystem, 2, 1, 1, 1)
        self.btn_SaveSystem = QtWidgets.QPushButton(self.frame)
        self.btn_SaveSystem.setMaximumSize(QtCore.QSize(16600000, 16777215))
        self.btn_SaveSystem.setObjectName("btn_SaveSystem")
        self.gridLayout_4.addWidget(self.btn_SaveSystem, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            510, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_4.addItem(spacerItem, 2, 3, 1, 1)
        self.gridLayout_5.addWidget(self.frame, 1, 0, 1, 1)
        self.groupBox_searchSubstance = QtWidgets.QGroupBox(self.tabSystem)
        self.groupBox_searchSubstance.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox_searchSubstance.setMaximumSize(QtCore.QSize(167772, 16777215))
        self.groupBox_searchSubstance.setObjectName("groupBox_searchSubstance")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_searchSubstance)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.le_searchSubstance = QtWidgets.QLineEdit(self.groupBox_searchSubstance)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.le_searchSubstance.sizePolicy().hasHeightForWidth()
        )
        self.le_searchSubstance.setSizePolicy(sizePolicy)
        self.le_searchSubstance.setMaximumSize(QtCore.QSize(160000, 23))
        self.le_searchSubstance.setText("")
        self.le_searchSubstance.setObjectName("le_searchSubstance")
        self.gridLayout_3.addWidget(self.le_searchSubstance, 0, 1, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(
            406, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_3.addItem(spacerItem1, 2, 4, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_searchSubstance)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 2, 0, 1, 2)
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
        self.gridLayout_3.addWidget(self.btn_searchSubstance, 0, 0, 1, 1)
        self.btn_Add = QtWidgets.QPushButton(self.groupBox_searchSubstance)
        self.btn_Add.setObjectName("btn_Add")
        self.gridLayout_3.addWidget(self.btn_Add, 2, 2, 1, 1)
        self.btn_Remove = QtWidgets.QPushButton(self.groupBox_searchSubstance)
        self.btn_Remove.setObjectName("btn_Remove")
        self.gridLayout_3.addWidget(self.btn_Remove, 2, 3, 1, 1)
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
        self.gridLayout_3.addWidget(self.tableWidget_searchSubstance, 1, 0, 1, 5)
        self.gridLayout_5.addWidget(self.groupBox_searchSubstance, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabSystem, "")
        self.tabCalculations = QtWidgets.QWidget()
        self.tabCalculations.setObjectName("tabCalculations")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.tabCalculations)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.frame_input = QtWidgets.QFrame(self.tabCalculations)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_input.sizePolicy().hasHeightForWidth())
        self.frame_input.setSizePolicy(sizePolicy)
        self.frame_input.setMinimumSize(QtCore.QSize(300, 0))
        self.frame_input.setMaximumSize(QtCore.QSize(16777000, 16777215))
        self.frame_input.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_input.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_input.setObjectName("frame_input")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_input)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.groupBox_EOS = QtWidgets.QGroupBox(self.frame_input)
        self.groupBox_EOS.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox_EOS.setObjectName("groupBox_EOS")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_EOS)
        self.gridLayout_7.setObjectName("gridLayout_7")
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
        self.gridLayout_7.addWidget(self.listWidget_eos_options, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_EOS, 0, 0, 1, 1)
        self.groupBox_processVariables = QtWidgets.QGroupBox(self.frame_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_processVariables.sizePolicy().hasHeightForWidth()
        )
        self.groupBox_processVariables.setSizePolicy(sizePolicy)
        self.groupBox_processVariables.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_processVariables.setMaximumSize(QtCore.QSize(16777215, 1000))
        self.groupBox_processVariables.setObjectName("groupBox_processVariables")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_processVariables)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox_processVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.le_procT = QtWidgets.QLineEdit(self.groupBox_processVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_procT.sizePolicy().hasHeightForWidth())
        self.le_procT.setSizePolicy(sizePolicy)
        self.le_procT.setInputMethodHints(
            QtCore.Qt.ImhDigitsOnly | QtCore.Qt.ImhPreferNumbers
        )
        self.le_procT.setObjectName("le_procT")
        self.horizontalLayout.addWidget(self.le_procT)
        self.comboBox_procTunit = QtWidgets.QComboBox(self.groupBox_processVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.comboBox_procTunit.sizePolicy().hasHeightForWidth()
        )
        self.comboBox_procTunit.setSizePolicy(sizePolicy)
        self.comboBox_procTunit.setObjectName("comboBox_procTunit")
        self.horizontalLayout.addWidget(self.comboBox_procTunit)
        self.gridLayout_8.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_processVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.le_procP = QtWidgets.QLineEdit(self.groupBox_processVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_procP.sizePolicy().hasHeightForWidth())
        self.le_procP.setSizePolicy(sizePolicy)
        self.le_procP.setObjectName("le_procP")
        self.horizontalLayout_2.addWidget(self.le_procP)
        self.comboBox_procPunit = QtWidgets.QComboBox(self.groupBox_processVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.comboBox_procPunit.sizePolicy().hasHeightForWidth()
        )
        self.comboBox_procPunit.setSizePolicy(sizePolicy)
        self.comboBox_procPunit.setObjectName("comboBox_procPunit")
        self.horizontalLayout_2.addWidget(self.comboBox_procPunit)
        self.gridLayout_8.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_processVariables, 1, 0, 1, 1)
        self.groupBox_refVariables = QtWidgets.QGroupBox(self.frame_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_refVariables.sizePolicy().hasHeightForWidth()
        )
        self.groupBox_refVariables.setSizePolicy(sizePolicy)
        self.groupBox_refVariables.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_refVariables.setMaximumSize(QtCore.QSize(16777215, 1000))
        self.groupBox_refVariables.setObjectName("groupBox_refVariables")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_refVariables)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_refVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.le_refT = QtWidgets.QLineEdit(self.groupBox_refVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_refT.sizePolicy().hasHeightForWidth())
        self.le_refT.setSizePolicy(sizePolicy)
        self.le_refT.setInputMethodHints(
            QtCore.Qt.ImhDigitsOnly | QtCore.Qt.ImhPreferNumbers
        )
        self.le_refT.setObjectName("le_refT")
        self.horizontalLayout_3.addWidget(self.le_refT)
        self.comboBox_refTunit = QtWidgets.QComboBox(self.groupBox_refVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.comboBox_refTunit.sizePolicy().hasHeightForWidth()
        )
        self.comboBox_refTunit.setSizePolicy(sizePolicy)
        self.comboBox_refTunit.setObjectName("comboBox_refTunit")
        self.horizontalLayout_3.addWidget(self.comboBox_refTunit)
        self.gridLayout_9.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_refVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.le_refP = QtWidgets.QLineEdit(self.groupBox_refVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_refP.sizePolicy().hasHeightForWidth())
        self.le_refP.setSizePolicy(sizePolicy)
        self.le_refP.setObjectName("le_refP")
        self.horizontalLayout_4.addWidget(self.le_refP)
        self.comboBox_refPunit = QtWidgets.QComboBox(self.groupBox_refVariables)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.comboBox_refPunit.sizePolicy().hasHeightForWidth()
        )
        self.comboBox_refPunit.setSizePolicy(sizePolicy)
        self.comboBox_refPunit.setObjectName("comboBox_refPunit")
        self.horizontalLayout_4.addWidget(self.comboBox_refPunit)
        self.gridLayout_9.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_refVariables, 2, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.frame_input)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.btn_units = QtWidgets.QPushButton(self.frame_2)
        self.btn_units.setObjectName("btn_units")
        self.gridLayout_10.addWidget(self.btn_units, 2, 1, 1, 1)
        self.btn_calculate = QtWidgets.QPushButton(self.frame_2)
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
        self.gridLayout_10.addWidget(self.btn_calculate, 2, 0, 1, 1)
        self.btn_savetxt = QtWidgets.QPushButton(self.frame_2)
        self.btn_savetxt.setObjectName("btn_savetxt")
        self.gridLayout_10.addWidget(self.btn_savetxt, 3, 1, 1, 1)
        self.gridLayout_6.addWidget(self.frame_2, 3, 0, 1, 1)
        self.gridLayout_11.addWidget(self.frame_input, 0, 0, 1, 1)
        self.frame_results = QtWidgets.QFrame(self.tabCalculations)
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
        self.groupBox_information.setMinimumSize(QtCore.QSize(0, 140))
        self.groupBox_information.setMaximumSize(QtCore.QSize(16777215, 250))
        self.groupBox_information.setObjectName("groupBox_information")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.groupBox_information)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.plainTextEdit_information = QtWidgets.QPlainTextEdit(
            self.groupBox_information
        )
        self.plainTextEdit_information.setMinimumSize(QtCore.QSize(0, 0))
        self.plainTextEdit_information.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.plainTextEdit_information.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plainTextEdit_information.setReadOnly(True)
        self.plainTextEdit_information.setObjectName("plainTextEdit_information")
        self.gridLayout_12.addWidget(self.plainTextEdit_information, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_information)
        self.groupBox_results = QtWidgets.QGroupBox(self.frame_results)
        self.groupBox_results.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox_results.setObjectName("groupBox_results")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox_results)
        self.gridLayout_13.setObjectName("gridLayout_13")
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
        self.gridLayout_13.addWidget(self.tableWidget_results, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_results)
        self.groupBox__log = QtWidgets.QGroupBox(self.frame_results)
        self.groupBox__log.setMinimumSize(QtCore.QSize(0, 150))
        self.groupBox__log.setMaximumSize(QtCore.QSize(16777215, 250))
        self.groupBox__log.setObjectName("groupBox__log")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox__log)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.plainTextEdit_log = QtWidgets.QPlainTextEdit(self.groupBox__log)
        self.plainTextEdit_log.setMaximumSize(QtCore.QSize(16777215, 166777))
        self.plainTextEdit_log.setReadOnly(True)
        self.plainTextEdit_log.setObjectName("plainTextEdit_log")
        self.gridLayout_14.addWidget(self.plainTextEdit_log, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox__log)
        self.gridLayout_11.addWidget(self.frame_results, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tabCalculations, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 4)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_2.addItem(spacerItem2, 1, 3, 1, 1)
        self.btn_EditBIParameters = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_EditBIParameters.setObjectName("btn_EditBIParameters")
        self.gridLayout_2.addWidget(self.btn_EditBIParameters, 1, 2, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(MixtureCalculationWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(
            self.le_searchSubstance,
            QtCore.SIGNAL("returnPressed()"),
            self.btn_searchSubstance.click,
        )
        QtCore.QObject.connect(
            self.tableWidget_searchSubstance,
            QtCore.SIGNAL("itemDoubleClicked(QTableWidgetItem*)"),
            self.btn_Add.click,
        )
        QtCore.QMetaObject.connectSlotsByName(MixtureCalculationWindow)

    def retranslateUi(self, MixtureCalculationWindow):
        MixtureCalculationWindow.setWindowTitle(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Mixture properties calculation", None, -1
            )
        )
        self.btn_VLE.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Vapor-liquid Equilibrium", None, -1
            )
        )
        self.tableWidget_MixtureSystem.horizontalHeaderItem(0).setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Name", None, -1
            )
        )
        self.tableWidget_MixtureSystem.horizontalHeaderItem(1).setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Formula", None, -1
            )
        )
        self.tableWidget_MixtureSystem.horizontalHeaderItem(2).setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Molar fraction", None, -1
            )
        )
        self.btn_setEquimolar.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Set equimolar system", None, -1
            )
        )
        self.btn_LoadSystem.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Load system", None, -1
            )
        )
        self.btn_SaveSystem.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Save system", None, -1
            )
        )
        self.groupBox_searchSubstance.setTitle(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Search substance", None, -1
            )
        )
        self.label.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Selected substances", None, -1
            )
        )
        self.btn_searchSubstance.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Search", None, -1
            )
        )
        self.btn_Add.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Add", None, -1
            )
        )
        self.btn_Remove.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Remove", None, -1
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabSystem),
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "System", None, -1
            ),
        )
        self.groupBox_EOS.setTitle(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Equation of state", None, -1
            )
        )
        self.groupBox_processVariables.setTitle(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Process variables", None, -1
            )
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate("MixtureCalculationWindow", "T", None, -1)
        )
        self.le_procT.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "150", None, -1
            )
        )
        self.label_3.setText(
            QtWidgets.QApplication.translate("MixtureCalculationWindow", "P", None, -1)
        )
        self.le_procP.setText(
            QtWidgets.QApplication.translate("MixtureCalculationWindow", "1", None, -1)
        )
        self.groupBox_refVariables.setTitle(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Reference variables", None, -1
            )
        )
        self.label_4.setText(
            QtWidgets.QApplication.translate("MixtureCalculationWindow", "T", None, -1)
        )
        self.le_refT.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "300", None, -1
            )
        )
        self.label_5.setText(
            QtWidgets.QApplication.translate("MixtureCalculationWindow", "P", None, -1)
        )
        self.le_refP.setText(
            QtWidgets.QApplication.translate("MixtureCalculationWindow", "1", None, -1)
        )
        self.btn_units.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Units", None, -1
            )
        )
        self.btn_calculate.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Calculate", None, -1
            )
        )
        self.btn_savetxt.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Save to txt", None, -1
            )
        )
        self.groupBox_information.setTitle(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Information", None, -1
            )
        )
        self.groupBox_results.setTitle(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Results", None, -1
            )
        )
        self.groupBox__log.setTitle(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Log", None, -1
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabCalculations),
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow", "Calculations", None, -1
            ),
        )
        self.btn_EditBIParameters.setText(
            QtWidgets.QApplication.translate(
                "MixtureCalculationWindow",
                "Edit binary interactions parameters",
                None,
                -1,
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MixtureCalculationWindow = QtWidgets.QWidget()
    ui = Ui_MixtureCalculationWindow()
    ui.setupUi(MixtureCalculationWindow)
    MixtureCalculationWindow.show()
    sys.exit(app.exec_())
