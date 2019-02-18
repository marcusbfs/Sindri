# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/db_substanceProperties_ui.ui',
# licensing of 'designer/db_substanceProperties_ui.ui' applies.
#
# Created: Fri Jan 11 18:18:07 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form_db_substanceProperties(object):
    def setupUi(self, Form_db_substanceProperties):
        Form_db_substanceProperties.setObjectName("Form_db_substanceProperties")
        Form_db_substanceProperties.setWindowModality(QtCore.Qt.ApplicationModal)
        Form_db_substanceProperties.resize(432, 316)
        self.gridLayout = QtWidgets.QGridLayout(Form_db_substanceProperties)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget_substanceProperties = QtWidgets.QTabWidget(
            Form_db_substanceProperties
        )
        self.tabWidget_substanceProperties.setAcceptDrops(False)
        self.tabWidget_substanceProperties.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget_substanceProperties.setAutoFillBackground(False)
        self.tabWidget_substanceProperties.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_substanceProperties.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_substanceProperties.setObjectName(
            "tabWidget_substanceProperties"
        )
        self.tab_identification = QtWidgets.QWidget()
        self.tab_identification.setObjectName("tab_identification")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_identification)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(5, -1, 20, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.tab_identification)
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.le_name = QtWidgets.QLineEdit(self.tab_identification)
        self.le_name.setMinimumSize(QtCore.QSize(146, 0))
        self.le_name.setInputMethodHints(QtCore.Qt.ImhNone)
        self.le_name.setText("")
        self.le_name.setCursorPosition(0)
        self.le_name.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.le_name.setObjectName("le_name")
        self.horizontalLayout_2.addWidget(self.le_name)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.tab_identification)
        self.label_2.setMinimumSize(QtCore.QSize(60, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.le_formula = QtWidgets.QLineEdit(self.tab_identification)
        self.le_formula.setMinimumSize(QtCore.QSize(146, 0))
        self.le_formula.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.le_formula.setObjectName("le_formula")
        self.horizontalLayout_3.addWidget(self.le_formula)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.tab_identification)
        self.label_3.setMinimumSize(QtCore.QSize(60, 0))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.le_CAS = QtWidgets.QLineEdit(self.tab_identification)
        self.le_CAS.setMinimumSize(QtCore.QSize(146, 0))
        self.le_CAS.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.le_CAS.setObjectName("le_CAS")
        self.horizontalLayout_4.addWidget(self.le_CAS)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget_substanceProperties.addTab(self.tab_identification, "")
        self.tab_generalData = QtWidgets.QWidget()
        self.tab_generalData.setObjectName("tab_generalData")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_generalData)
        self.verticalLayout_7.setContentsMargins(60, -1, 60, -1)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_4 = QtWidgets.QLabel(self.tab_generalData)
        self.label_4.setMinimumSize(QtCore.QSize(140, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_15.addWidget(self.label_4)
        self.le_MM = QtWidgets.QLineEdit(self.tab_generalData)
        self.le_MM.setMinimumSize(QtCore.QSize(70, 0))
        self.le_MM.setInputMethodHints(QtCore.Qt.ImhNone)
        self.le_MM.setObjectName("le_MM")
        self.horizontalLayout_15.addWidget(self.le_MM)
        self.label_5 = QtWidgets.QLabel(self.tab_generalData)
        self.label_5.setMinimumSize(QtCore.QSize(60, 0))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_15.addWidget(self.label_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_11 = QtWidgets.QLabel(self.tab_generalData)
        self.label_11.setMinimumSize(QtCore.QSize(140, 0))
        self.label_11.setTextFormat(QtCore.Qt.RichText)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_14.addWidget(self.label_11)
        self.le_Tfp = QtWidgets.QLineEdit(self.tab_generalData)
        self.le_Tfp.setMinimumSize(QtCore.QSize(70, 0))
        self.le_Tfp.setObjectName("le_Tfp")
        self.horizontalLayout_14.addWidget(self.le_Tfp)
        self.label_12 = QtWidgets.QLabel(self.tab_generalData)
        self.label_12.setMinimumSize(QtCore.QSize(60, 0))
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_14.addWidget(self.label_12)
        self.verticalLayout_6.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_13 = QtWidgets.QLabel(self.tab_generalData)
        self.label_13.setMinimumSize(QtCore.QSize(140, 0))
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_13.addWidget(self.label_13)
        self.le_Tb = QtWidgets.QLineEdit(self.tab_generalData)
        self.le_Tb.setMinimumSize(QtCore.QSize(70, 0))
        self.le_Tb.setObjectName("le_Tb")
        self.horizontalLayout_13.addWidget(self.le_Tb)
        self.label_14 = QtWidgets.QLabel(self.tab_generalData)
        self.label_14.setMinimumSize(QtCore.QSize(60, 0))
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_13.addWidget(self.label_14)
        self.verticalLayout_6.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_15 = QtWidgets.QLabel(self.tab_generalData)
        self.label_15.setMinimumSize(QtCore.QSize(140, 0))
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_12.addWidget(self.label_15)
        self.le_Tc = QtWidgets.QLineEdit(self.tab_generalData)
        self.le_Tc.setMinimumSize(QtCore.QSize(70, 0))
        self.le_Tc.setObjectName("le_Tc")
        self.horizontalLayout_12.addWidget(self.le_Tc)
        self.label_16 = QtWidgets.QLabel(self.tab_generalData)
        self.label_16.setMinimumSize(QtCore.QSize(60, 0))
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_12.addWidget(self.label_16)
        self.verticalLayout_6.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_17 = QtWidgets.QLabel(self.tab_generalData)
        self.label_17.setMinimumSize(QtCore.QSize(140, 0))
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_11.addWidget(self.label_17)
        self.le_Pc = QtWidgets.QLineEdit(self.tab_generalData)
        self.le_Pc.setMinimumSize(QtCore.QSize(70, 0))
        self.le_Pc.setObjectName("le_Pc")
        self.horizontalLayout_11.addWidget(self.le_Pc)
        self.label_18 = QtWidgets.QLabel(self.tab_generalData)
        self.label_18.setMinimumSize(QtCore.QSize(60, 0))
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_11.addWidget(self.label_18)
        self.verticalLayout_6.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_19 = QtWidgets.QLabel(self.tab_generalData)
        self.label_19.setMinimumSize(QtCore.QSize(140, 0))
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_10.addWidget(self.label_19)
        self.le_Vc = QtWidgets.QLineEdit(self.tab_generalData)
        self.le_Vc.setMinimumSize(QtCore.QSize(70, 0))
        self.le_Vc.setObjectName("le_Vc")
        self.horizontalLayout_10.addWidget(self.le_Vc)
        self.label_20 = QtWidgets.QLabel(self.tab_generalData)
        self.label_20.setMinimumSize(QtCore.QSize(60, 0))
        self.label_20.setTextFormat(QtCore.Qt.RichText)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_10.addWidget(self.label_20)
        self.verticalLayout_6.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_21 = QtWidgets.QLabel(self.tab_generalData)
        self.label_21.setMinimumSize(QtCore.QSize(140, 0))
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_9.addWidget(self.label_21)
        self.le_Zc = QtWidgets.QLineEdit(self.tab_generalData)
        self.le_Zc.setMinimumSize(QtCore.QSize(70, 0))
        self.le_Zc.setObjectName("le_Zc")
        self.horizontalLayout_9.addWidget(self.le_Zc)
        self.label_22 = QtWidgets.QLabel(self.tab_generalData)
        self.label_22.setMinimumSize(QtCore.QSize(60, 0))
        self.label_22.setText("")
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_9.addWidget(self.label_22)
        self.verticalLayout_6.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_23 = QtWidgets.QLabel(self.tab_generalData)
        self.label_23.setMinimumSize(QtCore.QSize(140, 0))
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_8.addWidget(self.label_23)
        self.le_omega = QtWidgets.QLineEdit(self.tab_generalData)
        self.le_omega.setMinimumSize(QtCore.QSize(70, 0))
        self.le_omega.setObjectName("le_omega")
        self.horizontalLayout_8.addWidget(self.le_omega)
        self.label_24 = QtWidgets.QLabel(self.tab_generalData)
        self.label_24.setMinimumSize(QtCore.QSize(60, 0))
        self.label_24.setText("")
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_8.addWidget(self.label_24)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.tabWidget_substanceProperties.addTab(self.tab_generalData, "")
        self.tab_Cp = QtWidgets.QWidget()
        self.tab_Cp.setObjectName("tab_Cp")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.tab_Cp)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_26 = QtWidgets.QLabel(self.tab_Cp)
        self.label_26.setTextFormat(QtCore.Qt.RichText)
        self.label_26.setWordWrap(True)
        self.label_26.setObjectName("label_26")
        self.verticalLayout_11.addWidget(self.label_26)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_25 = QtWidgets.QLabel(self.tab_Cp)
        self.label_25.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_16.addWidget(self.label_25)
        self.le_a0 = QtWidgets.QLineEdit(self.tab_Cp)
        self.le_a0.setMaximumSize(QtCore.QSize(70, 16777215))
        self.le_a0.setObjectName("le_a0")
        self.horizontalLayout_16.addWidget(self.le_a0)
        self.verticalLayout_8.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_30 = QtWidgets.QLabel(self.tab_Cp)
        self.label_30.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_20.addWidget(self.label_30)
        self.le_a1 = QtWidgets.QLineEdit(self.tab_Cp)
        self.le_a1.setMaximumSize(QtCore.QSize(70, 16777215))
        self.le_a1.setObjectName("le_a1")
        self.horizontalLayout_20.addWidget(self.le_a1)
        self.verticalLayout_8.addLayout(self.horizontalLayout_20)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_29 = QtWidgets.QLabel(self.tab_Cp)
        self.label_29.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_19.addWidget(self.label_29)
        self.le_a2 = QtWidgets.QLineEdit(self.tab_Cp)
        self.le_a2.setMaximumSize(QtCore.QSize(70, 16777215))
        self.le_a2.setObjectName("le_a2")
        self.horizontalLayout_19.addWidget(self.le_a2)
        self.verticalLayout_8.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_28 = QtWidgets.QLabel(self.tab_Cp)
        self.label_28.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_18.addWidget(self.label_28)
        self.le_a3 = QtWidgets.QLineEdit(self.tab_Cp)
        self.le_a3.setMaximumSize(QtCore.QSize(70, 16777215))
        self.le_a3.setObjectName("le_a3")
        self.horizontalLayout_18.addWidget(self.le_a3)
        self.verticalLayout_8.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_27 = QtWidgets.QLabel(self.tab_Cp)
        self.label_27.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_17.addWidget(self.label_27)
        self.le_a4 = QtWidgets.QLineEdit(self.tab_Cp)
        self.le_a4.setMaximumSize(QtCore.QSize(70, 16777215))
        self.le_a4.setObjectName("le_a4")
        self.horizontalLayout_17.addWidget(self.le_a4)
        self.verticalLayout_8.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_24.addLayout(self.verticalLayout_8)
        self.widget = QtWidgets.QWidget(self.tab_Cp)
        self.widget.setMinimumSize(QtCore.QSize(50, 0))
        self.widget.setMaximumSize(QtCore.QSize(1000, 300))
        self.widget.setObjectName("widget")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_31 = QtWidgets.QLabel(self.widget)
        self.label_31.setMaximumSize(QtCore.QSize(140, 16777215))
        self.label_31.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_31.setAutoFillBackground(False)
        self.label_31.setAlignment(QtCore.Qt.AlignCenter)
        self.label_31.setObjectName("label_31")
        self.verticalLayout_9.addWidget(self.label_31)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_32 = QtWidgets.QLabel(self.widget)
        self.label_32.setMinimumSize(QtCore.QSize(0, 0))
        self.label_32.setMaximumSize(QtCore.QSize(38, 16777215))
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_21.addWidget(self.label_32)
        self.le_CpTmin = QtWidgets.QLineEdit(self.widget)
        self.le_CpTmin.setMaximumSize(QtCore.QSize(40, 16777215))
        self.le_CpTmin.setObjectName("le_CpTmin")
        self.horizontalLayout_21.addWidget(self.le_CpTmin)
        self.horizontalLayout_23.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.label_33 = QtWidgets.QLabel(self.widget)
        self.label_33.setMaximumSize(QtCore.QSize(42, 16777215))
        self.label_33.setObjectName("label_33")
        self.horizontalLayout_22.addWidget(self.label_33)
        self.le_CpTmax = QtWidgets.QLineEdit(self.widget)
        self.le_CpTmax.setMinimumSize(QtCore.QSize(0, 0))
        self.le_CpTmax.setMaximumSize(QtCore.QSize(40, 16777215))
        self.le_CpTmax.setObjectName("le_CpTmax")
        self.horizontalLayout_22.addWidget(self.le_CpTmax)
        self.horizontalLayout_23.addLayout(self.horizontalLayout_22)
        self.verticalLayout_9.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_25.addLayout(self.verticalLayout_9)
        self.horizontalLayout_24.addWidget(self.widget)
        self.verticalLayout_11.addLayout(self.horizontalLayout_24)
        self.verticalLayout_12.addLayout(self.verticalLayout_11)
        self.tabWidget_substanceProperties.addTab(self.tab_Cp, "")
        self.tab_VaporPressure = QtWidgets.QWidget()
        self.tab_VaporPressure.setObjectName("tab_VaporPressure")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.tab_VaporPressure)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setContentsMargins(80, -1, 80, -1)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_34 = QtWidgets.QLabel(self.tab_VaporPressure)
        self.label_34.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_34.setAlignment(QtCore.Qt.AlignCenter)
        self.label_34.setObjectName("label_34")
        self.verticalLayout_13.addWidget(self.label_34)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_35 = QtWidgets.QLabel(self.tab_VaporPressure)
        self.label_35.setMaximumSize(QtCore.QSize(44, 16777215))
        self.label_35.setObjectName("label_35")
        self.horizontalLayout_26.addWidget(self.label_35)
        self.le_AntoineA = QtWidgets.QLineEdit(self.tab_VaporPressure)
        self.le_AntoineA.setMinimumSize(QtCore.QSize(40, 0))
        self.le_AntoineA.setMaximumSize(QtCore.QSize(100, 16777215))
        self.le_AntoineA.setObjectName("le_AntoineA")
        self.horizontalLayout_26.addWidget(self.le_AntoineA)
        self.verticalLayout_10.addLayout(self.horizontalLayout_26)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_36 = QtWidgets.QLabel(self.tab_VaporPressure)
        self.label_36.setMaximumSize(QtCore.QSize(44, 16777215))
        self.label_36.setObjectName("label_36")
        self.horizontalLayout_27.addWidget(self.label_36)
        self.le_AntoineB = QtWidgets.QLineEdit(self.tab_VaporPressure)
        self.le_AntoineB.setMinimumSize(QtCore.QSize(40, 0))
        self.le_AntoineB.setMaximumSize(QtCore.QSize(100, 16777215))
        self.le_AntoineB.setObjectName("le_AntoineB")
        self.horizontalLayout_27.addWidget(self.le_AntoineB)
        self.verticalLayout_10.addLayout(self.horizontalLayout_27)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_37 = QtWidgets.QLabel(self.tab_VaporPressure)
        self.label_37.setMaximumSize(QtCore.QSize(44, 16777215))
        self.label_37.setObjectName("label_37")
        self.horizontalLayout_28.addWidget(self.label_37)
        self.le_AntoineC = QtWidgets.QLineEdit(self.tab_VaporPressure)
        self.le_AntoineC.setMinimumSize(QtCore.QSize(40, 0))
        self.le_AntoineC.setMaximumSize(QtCore.QSize(100, 16777215))
        self.le_AntoineC.setObjectName("le_AntoineC")
        self.horizontalLayout_28.addWidget(self.le_AntoineC)
        self.verticalLayout_10.addLayout(self.horizontalLayout_28)
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.label_39 = QtWidgets.QLabel(self.tab_VaporPressure)
        self.label_39.setMaximumSize(QtCore.QSize(44, 16777215))
        self.label_39.setObjectName("label_39")
        self.horizontalLayout_30.addWidget(self.label_39)
        self.le_AntoineTmin = QtWidgets.QLineEdit(self.tab_VaporPressure)
        self.le_AntoineTmin.setMinimumSize(QtCore.QSize(40, 0))
        self.le_AntoineTmin.setMaximumSize(QtCore.QSize(100, 16777215))
        self.le_AntoineTmin.setObjectName("le_AntoineTmin")
        self.horizontalLayout_30.addWidget(self.le_AntoineTmin)
        self.verticalLayout_10.addLayout(self.horizontalLayout_30)
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.label_40 = QtWidgets.QLabel(self.tab_VaporPressure)
        self.label_40.setMaximumSize(QtCore.QSize(44, 16777215))
        self.label_40.setObjectName("label_40")
        self.horizontalLayout_31.addWidget(self.label_40)
        self.le_AntoineTmax = QtWidgets.QLineEdit(self.tab_VaporPressure)
        self.le_AntoineTmax.setMinimumSize(QtCore.QSize(40, 0))
        self.le_AntoineTmax.setMaximumSize(QtCore.QSize(100, 16777215))
        self.le_AntoineTmax.setObjectName("le_AntoineTmax")
        self.horizontalLayout_31.addWidget(self.le_AntoineTmax)
        self.verticalLayout_10.addLayout(self.horizontalLayout_31)
        self.verticalLayout_13.addLayout(self.verticalLayout_10)
        self.verticalLayout_14.addLayout(self.verticalLayout_13)
        spacerItem = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_14.addItem(spacerItem)
        self.tabWidget_substanceProperties.addTab(self.tab_VaporPressure, "")
        self.verticalLayout_3.addWidget(self.tabWidget_substanceProperties)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_edit_confirm = QtWidgets.QPushButton(Form_db_substanceProperties)
        self.btn_edit_confirm.setObjectName("btn_edit_confirm")
        self.horizontalLayout.addWidget(self.btn_edit_confirm)
        self.btn_edit_cancel = QtWidgets.QPushButton(Form_db_substanceProperties)
        self.btn_edit_cancel.setObjectName("btn_edit_cancel")
        self.horizontalLayout.addWidget(self.btn_edit_cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.retranslateUi(Form_db_substanceProperties)
        self.tabWidget_substanceProperties.setCurrentIndex(0)
        QtCore.QObject.connect(
            self.btn_edit_confirm,
            QtCore.SIGNAL("clicked()"),
            Form_db_substanceProperties.confirm_clicked,
        )
        QtCore.QObject.connect(
            self.btn_edit_cancel,
            QtCore.SIGNAL("clicked()"),
            Form_db_substanceProperties.cancel_clicked,
        )
        QtCore.QMetaObject.connectSlotsByName(Form_db_substanceProperties)

    def retranslateUi(self, Form_db_substanceProperties):
        Form_db_substanceProperties.setWindowTitle(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Substance properties", None, -1
            )
        )
        self.label.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Name", None, -1
            )
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Formula", None, -1
            )
        )
        self.label_3.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "CAS number", None, -1
            )
        )
        self.tabWidget_substanceProperties.setTabText(
            self.tabWidget_substanceProperties.indexOf(self.tab_identification),
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Identification", None, -1
            ),
        )
        self.label_4.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Molar weight", None, -1
            )
        )
        self.label_5.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "[g/mol]", None, -1
            )
        )
        self.label_11.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties",
                "<html><head/><body><p>Freezing point temp. (Tfp)</p></body></html>",
                None,
                -1,
            )
        )
        self.le_Tfp.setToolTip(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties",
                "<html><head/><body><p>Freezing point temperature</p></body></html>",
                None,
                -1,
            )
        )
        self.label_12.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "[K]", None, -1
            )
        )
        self.label_13.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Boiling temp. (Tb)", None, -1
            )
        )
        self.label_14.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "[K]", None, -1
            )
        )
        self.label_15.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Critical temp. (Tc)", None, -1
            )
        )
        self.label_16.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "[K]", None, -1
            )
        )
        self.label_17.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Critical pressure (Pc)", None, -1
            )
        )
        self.label_18.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "[bar]", None, -1
            )
        )
        self.label_19.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Critical volume (Vc)", None, -1
            )
        )
        self.label_20.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "[g/mol]", None, -1
            )
        )
        self.label_21.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Compressibility factor (Zc)", None, -1
            )
        )
        self.label_23.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Acentric factor", None, -1
            )
        )
        self.tabWidget_substanceProperties.setTabText(
            self.tabWidget_substanceProperties.indexOf(self.tab_generalData),
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "General data", None, -1
            ),
        )
        self.label_26.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties",
                '<html><head/><body><p align="center"><span style=" font-size:14pt; font-weight:600;">C</span><span style=" font-size:14pt; font-weight:600; vertical-align:sub;">p</span><span style=" font-size:14pt; font-weight:600; vertical-align:super;">0</span><span style=" font-size:14pt; font-weight:600;">/R = a0 + a1*T + a2*T</span><span style=" font-size:14pt; font-weight:600; vertical-align:super;">2</span><span style=" font-size:14pt; font-weight:600;"> + a3*T</span><span style=" font-size:14pt; font-weight:600; vertical-align:super;">3</span><span style=" font-size:14pt; font-weight:600;"> + a4*T</span><span style=" font-size:14pt; font-weight:600; vertical-align:super;">4</span></p></body></html>',
                None,
                -1,
            )
        )
        self.label_25.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "a0", None, -1
            )
        )
        self.label_30.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "a1", None, -1
            )
        )
        self.label_29.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "a2", None, -1
            )
        )
        self.label_28.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "a3", None, -1
            )
        )
        self.label_27.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "a4", None, -1
            )
        )
        self.label_31.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Temperature range", None, -1
            )
        )
        self.label_32.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Tmin [K]", None, -1
            )
        )
        self.label_33.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Tmax [K]", None, -1
            )
        )
        self.tabWidget_substanceProperties.setTabText(
            self.tabWidget_substanceProperties.indexOf(self.tab_Cp),
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Cp", None, -1
            ),
        )
        self.label_34.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Antoine", None, -1
            )
        )
        self.label_35.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "A", None, -1
            )
        )
        self.label_36.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "B", None, -1
            )
        )
        self.label_37.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "C", None, -1
            )
        )
        self.label_39.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Tmin [K]", None, -1
            )
        )
        self.label_40.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Tmax [K]", None, -1
            )
        )
        self.tabWidget_substanceProperties.setTabText(
            self.tabWidget_substanceProperties.indexOf(self.tab_VaporPressure),
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Vapor pressure", None, -1
            ),
        )
        self.btn_edit_confirm.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Confirm", None, -1
            )
        )
        self.btn_edit_cancel.setText(
            QtWidgets.QApplication.translate(
                "Form_db_substanceProperties", "Cancel", None, -1
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form_db_substanceProperties = QtWidgets.QWidget()
    ui = Ui_Form_db_substanceProperties()
    ui.setupUi(Form_db_substanceProperties)
    Form_db_substanceProperties.show()
    sys.exit(app.exec_())
