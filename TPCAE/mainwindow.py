from PySide2 import QtWidgets
from PySide2.QtCore import Slot
import db
from ui.mainwindow_ui import Ui_MainWindow
from databaseWindow import databaseWindow
from pureSubstanceCalculationsWindow import Window_PureSubstanceCalculations


class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.setupUi(self)
        self.dbw = databaseWindow()
        self.btn_PureSubstanceCalculations.clicked.connect(
            self.open_PureSubstanceCalculations
        )

    def open_db_window(self):
        self.dbw.show()

    @Slot()
    def open_PureSubstanceCalculations(self):
        self.pureSubsWin = Window_PureSubstanceCalculations()
        self.pureSubsWin.show()

    def closeEvent(self, *args, **kwargs):
        db.db.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())
