# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\db_substanceProperties_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_db_substanceProperties(object):
    def setupUi(self, Form_db_substanceProperties):
        Form_db_substanceProperties.setObjectName("Form_db_substanceProperties")
        Form_db_substanceProperties.resize(513, 452)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form_db_substanceProperties)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget_substanceProperties = QtWidgets.QTabWidget(Form_db_substanceProperties)
        self.tabWidget_substanceProperties.setAcceptDrops(False)
        self.tabWidget_substanceProperties.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget_substanceProperties.setAutoFillBackground(False)
        self.tabWidget_substanceProperties.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_substanceProperties.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_substanceProperties.setObjectName("tabWidget_substanceProperties")
        self.tab_identification = QtWidgets.QWidget()
        self.tab_identification.setObjectName("tab_identification")
        self.widget = QtWidgets.QWidget(self.tab_identification)
        self.widget.setGeometry(QtCore.QRect(0, 0, 471, 391))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(5, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.le_name = QtWidgets.QLineEdit(self.widget)
        self.le_name.setText("")
        self.le_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_name.setObjectName("le_name")
        self.horizontalLayout_2.addWidget(self.le_name)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.le_formula = QtWidgets.QLineEdit(self.widget)
        self.le_formula.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_formula.setObjectName("le_formula")
        self.horizontalLayout_3.addWidget(self.le_formula)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.le_CAS = QtWidgets.QLineEdit(self.widget)
        self.le_CAS.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_CAS.setObjectName("le_CAS")
        self.horizontalLayout_4.addWidget(self.le_CAS)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tabWidget_substanceProperties.addTab(self.tab_identification, "")
        self.tab_generalData = QtWidgets.QWidget()
        self.tab_generalData.setObjectName("tab_generalData")
        self.tabWidget_substanceProperties.addTab(self.tab_generalData, "")
        self.horizontalLayout.addWidget(self.tabWidget_substanceProperties)

        self.retranslateUi(Form_db_substanceProperties)
        self.tabWidget_substanceProperties.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form_db_substanceProperties)

    def retranslateUi(self, Form_db_substanceProperties):
        _translate = QtCore.QCoreApplication.translate
        Form_db_substanceProperties.setWindowTitle(_translate("Form_db_substanceProperties", "Substance properties"))
        self.label.setText(_translate("Form_db_substanceProperties", "Name"))
        self.label_2.setText(_translate("Form_db_substanceProperties", "Formula"))
        self.label_3.setText(_translate("Form_db_substanceProperties", "CAS number"))
        self.tabWidget_substanceProperties.setTabText(self.tabWidget_substanceProperties.indexOf(self.tab_identification), _translate("Form_db_substanceProperties", "Identification"))
        self.tabWidget_substanceProperties.setTabText(self.tabWidget_substanceProperties.indexOf(self.tab_generalData), _translate("Form_db_substanceProperties", "General data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_db_substanceProperties = QtWidgets.QWidget()
    ui = Ui_Form_db_substanceProperties()
    ui.setupUi(Form_db_substanceProperties)
    Form_db_substanceProperties.show()
    sys.exit(app.exec_())

