# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\db_substanceProperties_ui.ui',
# licensing of 'designer\db_substanceProperties_ui.ui' applies.
#
# Created: Wed Jan  9 12:23:50 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form_db_substanceProperties(object):
    def setupUi(self, Form_db_substanceProperties):
        Form_db_substanceProperties.setObjectName("Form_db_substanceProperties")
        Form_db_substanceProperties.setWindowModality(QtCore.Qt.ApplicationModal)
        Form_db_substanceProperties.resize(515, 380)
        self.gridLayout = QtWidgets.QGridLayout(Form_db_substanceProperties)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget_substanceProperties = QtWidgets.QTabWidget(Form_db_substanceProperties)
        self.tabWidget_substanceProperties.setAcceptDrops(False)
        self.tabWidget_substanceProperties.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget_substanceProperties.setAutoFillBackground(False)
        self.tabWidget_substanceProperties.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_substanceProperties.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_substanceProperties.setObjectName("tabWidget_substanceProperties")
        self.tab_identification = QtWidgets.QWidget()
        self.tab_identification.setObjectName("tab_identification")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_identification)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.tab_identification)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.le_name = QtWidgets.QLineEdit(self.tab_identification)
        self.le_name.setMinimumSize(QtCore.QSize(146, 0))
        self.le_name.setText("")
        self.le_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.le_name.setObjectName("le_name")
        self.horizontalLayout_2.addWidget(self.le_name)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label_2 = QtWidgets.QLabel(self.tab_identification)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.le_formula = QtWidgets.QLineEdit(self.tab_identification)
        self.le_formula.setMinimumSize(QtCore.QSize(146, 0))
        self.le_formula.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.le_formula.setObjectName("le_formula")
        self.horizontalLayout_3.addWidget(self.le_formula)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.label_3 = QtWidgets.QLabel(self.tab_identification)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.le_CAS = QtWidgets.QLineEdit(self.tab_identification)
        self.le_CAS.setMinimumSize(QtCore.QSize(146, 0))
        self.le_CAS.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.le_CAS.setObjectName("le_CAS")
        self.horizontalLayout_4.addWidget(self.le_CAS)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget_substanceProperties.addTab(self.tab_identification, "")
        self.tab_generalData = QtWidgets.QWidget()
        self.tab_generalData.setObjectName("tab_generalData")
        self.tabWidget_substanceProperties.addTab(self.tab_generalData, "")
        self.gridLayout.addWidget(self.tabWidget_substanceProperties, 0, 0, 1, 1)

        self.retranslateUi(Form_db_substanceProperties)
        self.tabWidget_substanceProperties.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form_db_substanceProperties)

    def retranslateUi(self, Form_db_substanceProperties):
        Form_db_substanceProperties.setWindowTitle(QtWidgets.QApplication.translate("Form_db_substanceProperties", "Substance properties", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form_db_substanceProperties", "Name", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form_db_substanceProperties", "Formula", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form_db_substanceProperties", "CAS number", None, -1))
        self.tabWidget_substanceProperties.setTabText(self.tabWidget_substanceProperties.indexOf(self.tab_identification), QtWidgets.QApplication.translate("Form_db_substanceProperties", "Identification", None, -1))
        self.tabWidget_substanceProperties.setTabText(self.tabWidget_substanceProperties.indexOf(self.tab_generalData), QtWidgets.QApplication.translate("Form_db_substanceProperties", "General data", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_db_substanceProperties = QtWidgets.QWidget()
    ui = Ui_Form_db_substanceProperties()
    ui.setupUi(Form_db_substanceProperties)
    Form_db_substanceProperties.show()
    sys.exit(app.exec_())

