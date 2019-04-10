# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/binary_interaction_parameters_ui.ui',
# licensing of 'designer/binary_interaction_parameters_ui.ui' applies.
#
# Created: Wed Apr 10 10:49:34 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_FormBinaryParameters(object):
    def setupUi(self, FormBinaryParameters):
        FormBinaryParameters.setObjectName("FormBinaryParameters")
        FormBinaryParameters.setWindowModality(QtCore.Qt.ApplicationModal)
        FormBinaryParameters.resize(555, 328)
        self.gridLayout = QtWidgets.QGridLayout(FormBinaryParameters)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(FormBinaryParameters)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 535, 308))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_cancel = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridLayout_2.addWidget(self.btn_cancel, 3, 4, 1, 1)
        self.btn_setZero = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_setZero.setObjectName("btn_setZero")
        self.gridLayout_2.addWidget(self.btn_setZero, 1, 4, 1, 1)
        self.btn_ok = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_ok.setObjectName("btn_ok")
        self.gridLayout_2.addWidget(self.btn_ok, 3, 3, 1, 1)
        self.btn_setSymmetric = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_setSymmetric.setObjectName("btn_setSymmetric")
        self.gridLayout_2.addWidget(self.btn_setSymmetric, 1, 3, 1, 1)
        self.tableWidget_BinaryParameters = QtWidgets.QTableWidget(
            self.scrollAreaWidgetContents
        )
        self.tableWidget_BinaryParameters.setMinimumSize(QtCore.QSize(400, 150))
        self.tableWidget_BinaryParameters.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_BinaryParameters.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget_BinaryParameters.setAlternatingRowColors(True)
        self.tableWidget_BinaryParameters.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.tableWidget_BinaryParameters.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectItems
        )
        self.tableWidget_BinaryParameters.setShowGrid(True)
        self.tableWidget_BinaryParameters.setRowCount(0)
        self.tableWidget_BinaryParameters.setColumnCount(0)
        self.tableWidget_BinaryParameters.setObjectName("tableWidget_BinaryParameters")
        self.tableWidget_BinaryParameters.setColumnCount(0)
        self.tableWidget_BinaryParameters.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget_BinaryParameters, 0, 0, 1, 5)
        spacerItem = QtWidgets.QSpacerItem(
            352, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(FormBinaryParameters)
        QtCore.QMetaObject.connectSlotsByName(FormBinaryParameters)

    def retranslateUi(self, FormBinaryParameters):
        FormBinaryParameters.setWindowTitle(
            QtWidgets.QApplication.translate(
                "FormBinaryParameters", "Binary interaction parameters", None, -1
            )
        )
        self.btn_cancel.setText(
            QtWidgets.QApplication.translate("FormBinaryParameters", "Cancel", None, -1)
        )
        self.btn_setZero.setText(
            QtWidgets.QApplication.translate(
                "FormBinaryParameters", "Set all values to zero", None, -1
            )
        )
        self.btn_ok.setText(
            QtWidgets.QApplication.translate("FormBinaryParameters", "Ok", None, -1)
        )
        self.btn_setSymmetric.setText(
            QtWidgets.QApplication.translate(
                "FormBinaryParameters", "Set symmetric", None, -1
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    FormBinaryParameters = QtWidgets.QWidget()
    ui = Ui_FormBinaryParameters()
    ui.setupUi(FormBinaryParameters)
    FormBinaryParameters.show()
    sys.exit(app.exec_())
