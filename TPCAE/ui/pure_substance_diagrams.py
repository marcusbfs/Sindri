# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/pure_substance_diagrams.ui',
# licensing of 'designer/pure_substance_diagrams.ui' applies.
#
# Created: Wed Feb 20 19:40:59 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form_PureSubstanceDiagrams(object):
    def setupUi(self, Form_PureSubstanceDiagrams):
        Form_PureSubstanceDiagrams.setObjectName("Form_PureSubstanceDiagrams")
        Form_PureSubstanceDiagrams.setWindowModality(QtCore.Qt.ApplicationModal)
        Form_PureSubstanceDiagrams.resize(318, 187)
        self.gridLayout = QtWidgets.QGridLayout(Form_PureSubstanceDiagrams)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form_PureSubstanceDiagrams)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_diagram = QtWidgets.QComboBox(Form_PureSubstanceDiagrams)
        self.comboBox_diagram.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox_diagram.setObjectName("comboBox_diagram")
        self.horizontalLayout.addWidget(self.comboBox_diagram)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form_PureSubstanceDiagrams)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.le_Ti = QtWidgets.QLineEdit(Form_PureSubstanceDiagrams)
        self.le_Ti.setObjectName("le_Ti")
        self.horizontalLayout_2.addWidget(self.le_Ti)
        self.label_3 = QtWidgets.QLabel(Form_PureSubstanceDiagrams)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.le_Tf = QtWidgets.QLineEdit(Form_PureSubstanceDiagrams)
        self.le_Tf.setObjectName("le_Tf")
        self.horizontalLayout_2.addWidget(self.le_Tf)
        self.comboBox_TrangeUnit = QtWidgets.QComboBox(Form_PureSubstanceDiagrams)
        self.comboBox_TrangeUnit.setObjectName("comboBox_TrangeUnit")
        self.horizontalLayout_2.addWidget(self.comboBox_TrangeUnit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(Form_PureSubstanceDiagrams)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.le_points = QtWidgets.QLineEdit(Form_PureSubstanceDiagrams)
        self.le_points.setObjectName("le_points")
        self.horizontalLayout_3.addWidget(self.le_points)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_yUnits = QtWidgets.QLabel(Form_PureSubstanceDiagrams)
        self.label_yUnits.setObjectName("label_yUnits")
        self.horizontalLayout_4.addWidget(self.label_yUnits)
        self.comboBox_yUnits = QtWidgets.QComboBox(Form_PureSubstanceDiagrams)
        self.comboBox_yUnits.setObjectName("comboBox_yUnits")
        self.horizontalLayout_4.addWidget(self.comboBox_yUnits)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_xUnits = QtWidgets.QLabel(Form_PureSubstanceDiagrams)
        self.label_xUnits.setObjectName("label_xUnits")
        self.horizontalLayout_5.addWidget(self.label_xUnits)
        self.comboBox_xUnits = QtWidgets.QComboBox(Form_PureSubstanceDiagrams)
        self.comboBox_xUnits.setObjectName("comboBox_xUnits")
        self.horizontalLayout_5.addWidget(self.comboBox_xUnits)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBox_xlogscale = QtWidgets.QCheckBox(Form_PureSubstanceDiagrams)
        self.checkBox_xlogscale.setObjectName("checkBox_xlogscale")
        self.gridLayout_2.addWidget(self.checkBox_xlogscale, 4, 0, 1, 1)
        self.checkBox_ylogscale = QtWidgets.QCheckBox(Form_PureSubstanceDiagrams)
        self.checkBox_ylogscale.setObjectName("checkBox_ylogscale")
        self.gridLayout_2.addWidget(self.checkBox_ylogscale, 2, 0, 1, 1)
        self.checkBox_smooth = QtWidgets.QCheckBox(Form_PureSubstanceDiagrams)
        self.checkBox_smooth.setObjectName("checkBox_smooth")
        self.gridLayout_2.addWidget(self.checkBox_smooth, 2, 1, 1, 1)
        self.checkBox_grid = QtWidgets.QCheckBox(Form_PureSubstanceDiagrams)
        self.checkBox_grid.setObjectName("checkBox_grid")
        self.gridLayout_2.addWidget(self.checkBox_grid, 4, 1, 1, 1)
        self.horizontalLayout_7.addLayout(self.gridLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_7, 3, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.btn_gen = QtWidgets.QPushButton(Form_PureSubstanceDiagrams)
        self.btn_gen.setObjectName("btn_gen")
        self.horizontalLayout_6.addWidget(self.btn_gen)
        self.btn_plot = QtWidgets.QPushButton(Form_PureSubstanceDiagrams)
        self.btn_plot.setObjectName("btn_plot")
        self.horizontalLayout_6.addWidget(self.btn_plot)
        self.gridLayout.addLayout(self.horizontalLayout_6, 4, 0, 1, 1)

        self.retranslateUi(Form_PureSubstanceDiagrams)
        QtCore.QMetaObject.connectSlotsByName(Form_PureSubstanceDiagrams)

    def retranslateUi(self, Form_PureSubstanceDiagrams):
        Form_PureSubstanceDiagrams.setWindowTitle(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "Pure Substance Diagrams", None, -1
            )
        )
        self.label.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "Diagram: ", None, -1
            )
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "Temperature range", None, -1
            )
        )
        self.label_3.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "-", None, -1
            )
        )
        self.label_4.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "Number of points", None, -1
            )
        )
        self.le_points.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "25", None, -1
            )
        )
        self.label_yUnits.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "Y unit", None, -1
            )
        )
        self.label_xUnits.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "X unit", None, -1
            )
        )
        self.checkBox_xlogscale.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "X log scale", None, -1
            )
        )
        self.checkBox_ylogscale.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "Y log scale", None, -1
            )
        )
        self.checkBox_smooth.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "Smooth curve", None, -1
            )
        )
        self.checkBox_grid.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "Grid", None, -1
            )
        )
        self.btn_gen.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "Generate data", None, -1
            )
        )
        self.btn_plot.setText(
            QtWidgets.QApplication.translate(
                "Form_PureSubstanceDiagrams", "Plot", None, -1
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form_PureSubstanceDiagrams = QtWidgets.QWidget()
    ui = Ui_Form_PureSubstanceDiagrams()
    ui.setupUi(Form_PureSubstanceDiagrams)
    Form_PureSubstanceDiagrams.show()
    sys.exit(app.exec_())