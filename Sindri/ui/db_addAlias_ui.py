# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/db_addAlias_ui.ui',
# licensing of 'designer/db_addAlias_ui.ui' applies.
#
# Created: Sun Apr 28 16:29:05 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form_AddAlias(object):
    def setupUi(self, Form_AddAlias):
        Form_AddAlias.setObjectName("Form_AddAlias")
        Form_AddAlias.setWindowModality(QtCore.Qt.ApplicationModal)
        Form_AddAlias.resize(180, 76)
        self.gridLayout = QtWidgets.QGridLayout(Form_AddAlias)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(Form_AddAlias)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(
            47, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.btn_ok = QtWidgets.QPushButton(Form_AddAlias)
        self.btn_ok.setObjectName("btn_ok")
        self.gridLayout.addWidget(self.btn_ok, 2, 1, 1, 1)
        self.btn_cancel = QtWidgets.QPushButton(Form_AddAlias)
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridLayout.addWidget(self.btn_cancel, 2, 2, 1, 1)
        self.le_alias = QtWidgets.QLineEdit(Form_AddAlias)
        self.le_alias.setObjectName("le_alias")
        self.gridLayout.addWidget(self.le_alias, 0, 0, 1, 3)

        self.retranslateUi(Form_AddAlias)
        QtCore.QObject.connect(
            self.le_alias, QtCore.SIGNAL("returnPressed()"), self.btn_ok.click
        )
        QtCore.QMetaObject.connectSlotsByName(Form_AddAlias)

    def retranslateUi(self, Form_AddAlias):
        Form_AddAlias.setWindowTitle(
            QtWidgets.QApplication.translate("Form_AddAlias", "Add alias", None, -1)
        )
        self.btn_ok.setText(
            QtWidgets.QApplication.translate("Form_AddAlias", "Ok", None, -1)
        )
        self.btn_cancel.setText(
            QtWidgets.QApplication.translate("Form_AddAlias", "Cancel", None, -1)
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form_AddAlias = QtWidgets.QWidget()
    ui = Ui_Form_AddAlias()
    ui.setupUi(Form_AddAlias)
    Form_AddAlias.show()
    sys.exit(app.exec_())
