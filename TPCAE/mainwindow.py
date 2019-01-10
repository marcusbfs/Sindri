from PySide2 import QtCore, QtGui, QtWidgets
from ui.mainwindow_ui import Ui_MainWindow
from databaseWindow import databaseWindow
import db


class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # QtWidgets.QMainWindow.__init__(self)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        super(mainwindow, self).__init__()
        self.setupUi(self)
        self.dbw = databaseWindow()
        # self.setWindowFlag(self, )

    def open_db_window(self):
        self.dbw.show()

    def closeEvent(self, *args, **kwargs):
        db.db.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())
