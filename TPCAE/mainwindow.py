from PySide2 import QtWidgets
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


class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.setupUi(self)
        self.dbw = databaseWindow()
        self.btn_PureSubstanceCalculations.clicked.connect(
            self.open_PureSubstanceCalculations
        )
        self.btn_MixtureCalculations.clicked.connect(self.open_MixtureCalculations)
        self.btn_about.clicked.connect(self.open_AboutWindow)
        self.setWindowTitle(_devinfo.__SOFTWARE_NAME__)

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
