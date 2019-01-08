from PyQt5 import QtCore, QtGui, QtWidgets
from ui.mainwindow_ui import Ui_MainWindow
from db import databaseWindow


class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # QtWidgets.QMainWindow.__init__(self)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        super(mainwindow, self).__init__()
        self.setupUi(self)

    def open_db_window(self):
        self.dbw = databaseWindow()
        self.dbw.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())
