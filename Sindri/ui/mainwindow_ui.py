# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/mainwindow_ui.ui',
# licensing of 'designer/mainwindow_ui.ui' applies.
#
# Created: Sun Jun  2 16:58:57 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(317, 342)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_main_title = QtWidgets.QLabel(self.centralwidget)
        self.label_main_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_main_title.setWordWrap(True)
        self.label_main_title.setObjectName("label_main_title")
        self.gridLayout.addWidget(self.label_main_title, 1, 0, 1, 1)
        self.btn_MixtureCalculations = QtWidgets.QPushButton(self.centralwidget)
        self.btn_MixtureCalculations.setObjectName("btn_MixtureCalculations")
        self.gridLayout.addWidget(self.btn_MixtureCalculations, 7, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.label_main_subtitle = QtWidgets.QLabel(self.centralwidget)
        self.label_main_subtitle.setAlignment(QtCore.Qt.AlignCenter)
        self.label_main_subtitle.setWordWrap(True)
        self.label_main_subtitle.setObjectName("label_main_subtitle")
        self.gridLayout.addWidget(self.label_main_subtitle, 2, 0, 1, 1)
        self.btn_PureSubstanceCalculations = QtWidgets.QPushButton(self.centralwidget)
        self.btn_PureSubstanceCalculations.setObjectName(
            "btn_PureSubstanceCalculations"
        )
        self.gridLayout.addWidget(self.btn_PureSubstanceCalculations, 6, 0, 1, 1)
        self.btn_about = QtWidgets.QPushButton(self.centralwidget)
        self.btn_about.setObjectName("btn_about")
        self.gridLayout.addWidget(self.btn_about, 8, 0, 1, 1)
        self.label_main_icon = QtWidgets.QLabel(self.centralwidget)
        self.label_main_icon.setText("")
        self.label_main_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.label_main_icon.setObjectName("label_main_icon")
        self.gridLayout.addWidget(self.label_main_icon, 0, 0, 1, 1)
        self.btn_BancoDeDados = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_BancoDeDados.sizePolicy().hasHeightForWidth()
        )
        self.btn_BancoDeDados.setSizePolicy(sizePolicy)
        self.btn_BancoDeDados.setMaximumSize(QtCore.QSize(16777211, 16777215))
        self.btn_BancoDeDados.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_BancoDeDados.setObjectName("btn_BancoDeDados")
        self.gridLayout.addWidget(self.btn_BancoDeDados, 4, 0, 1, 1)
        self.label_software_version = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_software_version.sizePolicy().hasHeightForWidth()
        )
        self.label_software_version.setSizePolicy(sizePolicy)
        self.label_software_version.setText("")
        self.label_software_version.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_software_version.setObjectName("label_software_version")
        self.gridLayout.addWidget(self.label_software_version, 9, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 317, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(
            self.btn_BancoDeDados, QtCore.SIGNAL("clicked()"), MainWindow.open_db_window
        )
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtWidgets.QApplication.translate(
                "MainWindow", "Sindri - Jump Start", None, -1
            )
        )
        self.label_main_title.setText(
            QtWidgets.QApplication.translate("MainWindow", "TextLabel", None, -1)
        )
        self.btn_MixtureCalculations.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Mixture calculations", None, -1
            )
        )
        self.label_main_subtitle.setText(
            QtWidgets.QApplication.translate("MainWindow", "TextLabel", None, -1)
        )
        self.btn_PureSubstanceCalculations.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Pure substance calculations", None, -1
            )
        )
        self.btn_about.setText(
            QtWidgets.QApplication.translate("MainWindow", "About", None, -1)
        )
        self.btn_BancoDeDados.setText(
            QtWidgets.QApplication.translate("MainWindow", "Database", None, -1)
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
