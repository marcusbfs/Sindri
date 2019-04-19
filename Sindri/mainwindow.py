from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Slot

import _devinfo
import db
from Controllers.MixtureCalculationsController import MixtureCalculationsController
from Controllers.PureSubstanceController import PureSubstanceController
from Models.MixtureModel import MixtureModel
from Models.PureSubstanceModel import PureSubstanceModel
from aboutWindow import Window_About
from databaseWindow import databaseWindow
from ui.mainwindow_ui import Ui_MainWindow
import resources.icons_rc


class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.setupUi(self)
        self.dbw = databaseWindow()
        self.btn_PureSubstanceCalculations.clicked.connect(
            self.open_PureSubstanceCalculations
        )

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/images/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.setWindowIcon(icon)

        self.btn_MixtureCalculations.clicked.connect(self.open_MixtureCalculations)
        self.btn_about.clicked.connect(self.open_AboutWindow)
        self.setWindowTitle(_devinfo.__SOFTWARE_NAME__)

        # button icons
        self.btn_BancoDeDados.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/database_button.png")))
        self.btn_about.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/about_button.png")))
        self.btn_PureSubstanceCalculations.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/pureSubstance_button.png")))
        self.btn_MixtureCalculations.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/mixture_button.png")))

    def open_db_window(self):
        self.dbw.show()

    @Slot()
    def open_PureSubstanceCalculations(self):
        self.pureSubstanceController = PureSubstanceController(PureSubstanceModel())
        self.pureSubstanceController.createMainView()

    @Slot()
    def open_MixtureCalculations(self):
        self.mixtureCalculationsController = MixtureCalculationsController(
            MixtureModel()
        )
        self.mixtureCalculationsController.createMixtureCalcView()

    @Slot()
    def open_AboutWindow(self):
        self.aboutWin = Window_About()
        self.aboutWin.show()

    def closeEvent(self, *args, **kwargs):
        db.db.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())
