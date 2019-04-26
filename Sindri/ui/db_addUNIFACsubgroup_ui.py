# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/db_addUNIFACsubgroup_ui.ui',
# licensing of 'designer/db_addUNIFACsubgroup_ui.ui' applies.
#
# Created: Fri Apr 26 13:16:48 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form_addUNIFACsubgroup(object):
    def setupUi(self, Form_addUNIFACsubgroup):
        Form_addUNIFACsubgroup.setObjectName("Form_addUNIFACsubgroup")
        Form_addUNIFACsubgroup.setWindowModality(QtCore.Qt.ApplicationModal)
        Form_addUNIFACsubgroup.resize(255, 102)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            Form_addUNIFACsubgroup.sizePolicy().hasHeightForWidth()
        )
        Form_addUNIFACsubgroup.setSizePolicy(sizePolicy)
        Form_addUNIFACsubgroup.setMaximumSize(QtCore.QSize(300, 102))
        self.gridLayout = QtWidgets.QGridLayout(Form_addUNIFACsubgroup)
        self.gridLayout.setObjectName("gridLayout")
        self.spinBox_UNIFACsubgroup_frequency = QtWidgets.QSpinBox(
            Form_addUNIFACsubgroup
        )
        self.spinBox_UNIFACsubgroup_frequency.setMinimum(1)
        self.spinBox_UNIFACsubgroup_frequency.setObjectName(
            "spinBox_UNIFACsubgroup_frequency"
        )
        self.gridLayout.addWidget(self.spinBox_UNIFACsubgroup_frequency, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form_addUNIFACsubgroup)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.btn_addUNIFACsubgroup_confirm = QtWidgets.QPushButton(
            Form_addUNIFACsubgroup
        )
        self.btn_addUNIFACsubgroup_confirm.setObjectName(
            "btn_addUNIFACsubgroup_confirm"
        )
        self.gridLayout.addWidget(self.btn_addUNIFACsubgroup_confirm, 3, 1, 1, 1)
        self.comboBox_UNIFACsubgroup = QtWidgets.QComboBox(Form_addUNIFACsubgroup)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.comboBox_UNIFACsubgroup.sizePolicy().hasHeightForWidth()
        )
        self.comboBox_UNIFACsubgroup.setSizePolicy(sizePolicy)
        self.comboBox_UNIFACsubgroup.setObjectName("comboBox_UNIFACsubgroup")
        self.gridLayout.addWidget(self.comboBox_UNIFACsubgroup, 0, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(Form_addUNIFACsubgroup)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.btn_addUNIFACsubgroup_cancel = QtWidgets.QPushButton(
            Form_addUNIFACsubgroup
        )
        self.btn_addUNIFACsubgroup_cancel.setObjectName("btn_addUNIFACsubgroup_cancel")
        self.gridLayout.addWidget(self.btn_addUNIFACsubgroup_cancel, 3, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.line = QtWidgets.QFrame(Form_addUNIFACsubgroup)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 3)

        self.retranslateUi(Form_addUNIFACsubgroup)
        QtCore.QMetaObject.connectSlotsByName(Form_addUNIFACsubgroup)

    def retranslateUi(self, Form_addUNIFACsubgroup):
        Form_addUNIFACsubgroup.setWindowTitle(
            QtWidgets.QApplication.translate(
                "Form_addUNIFACsubgroup", "UNIFAC Subgroups", None, -1
            )
        )
        self.label.setText(
            QtWidgets.QApplication.translate(
                "Form_addUNIFACsubgroup", "Subgroup", None, -1
            )
        )
        self.btn_addUNIFACsubgroup_confirm.setText(
            QtWidgets.QApplication.translate("Form_addUNIFACsubgroup", "Ok", None, -1)
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate(
                "Form_addUNIFACsubgroup", "Frequency", None, -1
            )
        )
        self.btn_addUNIFACsubgroup_cancel.setText(
            QtWidgets.QApplication.translate(
                "Form_addUNIFACsubgroup", "Cancel", None, -1
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form_addUNIFACsubgroup = QtWidgets.QWidget()
    ui = Ui_Form_addUNIFACsubgroup()
    ui.setupUi(Form_addUNIFACsubgroup)
    Form_addUNIFACsubgroup.show()
    sys.exit(app.exec_())
