# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/units_options_ui.ui',
# licensing of 'designer/units_options_ui.ui' applies.
#
# Created: Fri Aug 30 19:11:16 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form_UnitsOptions(object):
    def setupUi(self, Form_UnitsOptions):
        Form_UnitsOptions.setObjectName("Form_UnitsOptions")
        Form_UnitsOptions.setWindowModality(QtCore.Qt.ApplicationModal)
        Form_UnitsOptions.resize(290, 290)
        Form_UnitsOptions.setMinimumSize(QtCore.QSize(290, 290))
        self.gridLayout_2 = QtWidgets.QGridLayout(Form_UnitsOptions)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(Form_UnitsOptions)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 270, 270))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMaximumSize(QtCore.QSize(16777000, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox_pressure = QtWidgets.QComboBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.comboBox_pressure.sizePolicy().hasHeightForWidth()
        )
        self.comboBox_pressure.setSizePolicy(sizePolicy)
        self.comboBox_pressure.setObjectName("comboBox_pressure")
        self.verticalLayout.addWidget(self.comboBox_pressure)
        self.comboBox_temperature = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_temperature.setObjectName("comboBox_temperature")
        self.verticalLayout.addWidget(self.comboBox_temperature)
        self.comboBox_volume = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_volume.setObjectName("comboBox_volume")
        self.verticalLayout.addWidget(self.comboBox_volume)
        self.comboBox_density = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_density.setObjectName("comboBox_density")
        self.verticalLayout.addWidget(self.comboBox_density)
        self.comboBox_energ_per_mol = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_energ_per_mol.setObjectName("comboBox_energ_per_mol")
        self.verticalLayout.addWidget(self.comboBox_energ_per_mol)
        self.comboBox_energ_per_mol_temp = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_energ_per_mol_temp.setObjectName("comboBox_energ_per_mol_temp")
        self.verticalLayout.addWidget(self.comboBox_energ_per_mol_temp)
        self.gridLayout.addWidget(self.frame_2, 0, 1, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 47))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.btn_ok = QtWidgets.QPushButton(self.frame_3)
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout.addWidget(self.btn_ok)
        self.btn_cancel = QtWidgets.QPushButton(self.frame_3)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Form_UnitsOptions)
        QtCore.QMetaObject.connectSlotsByName(Form_UnitsOptions)

    def retranslateUi(self, Form_UnitsOptions):
        Form_UnitsOptions.setWindowTitle(
            QtWidgets.QApplication.translate("Form_UnitsOptions", "Units", None, -1)
        )
        self.label.setText(
            QtWidgets.QApplication.translate("Form_UnitsOptions", "Pressure", None, -1)
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate(
                "Form_UnitsOptions", "Temperature", None, -1
            )
        )
        self.label_3.setText(
            QtWidgets.QApplication.translate(
                "Form_UnitsOptions", "Molar volume", None, -1
            )
        )
        self.label_4.setText(
            QtWidgets.QApplication.translate("Form_UnitsOptions", "Density", None, -1)
        )
        self.label_5.setText(
            QtWidgets.QApplication.translate(
                "Form_UnitsOptions", "Energy per mol", None, -1
            )
        )
        self.label_6.setText(
            QtWidgets.QApplication.translate(
                "Form_UnitsOptions", "Energ. per mol temp.", None, -1
            )
        )
        self.btn_ok.setText(
            QtWidgets.QApplication.translate("Form_UnitsOptions", "Ok", None, -1)
        )
        self.btn_cancel.setText(
            QtWidgets.QApplication.translate("Form_UnitsOptions", "Cancel", None, -1)
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form_UnitsOptions = QtWidgets.QWidget()
    ui = Ui_Form_UnitsOptions()
    ui.setupUi(Form_UnitsOptions)
    Form_UnitsOptions.show()
    sys.exit(app.exec_())
