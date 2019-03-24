from PySide2 import QtWidgets
from PySide2.QtCore import Slot
import db
from ui.mainwindow_ui import Ui_MainWindow
from databaseWindow import databaseWindow
from pureSubstanceCalculationsWindow import Window_PureSubstanceCalculations
from mixtureCalculationsWindow import Window_MixtureCalculations
import _devinfo


class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.setupUi(self)
        self.dbw = databaseWindow()
        self.btn_PureSubstanceCalculations.clicked.connect(
            self.open_PureSubstanceCalculations
        )
        self.btn_MixtureCalculations.clicked.connect(self.open_MixtureCalculations)
        self.setWindowTitle(_devinfo.__SOFTWARE_NAME__)

    def open_db_window(self):
        self.dbw.show()

    @Slot()
    def open_PureSubstanceCalculations(self):
        self.pureSubsWin = Window_PureSubstanceCalculations()
        self.pureSubsWin.show()

    @Slot()
    def open_MixtureCalculations(self):
        self.MixCalcWin = Window_MixtureCalculations()
        self.MixCalcWin.show()

    def closeEvent(self, *args, **kwargs):
        db.db.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())
