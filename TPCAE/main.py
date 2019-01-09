import sys
from mainwindow import mainwindow
from PyQt5 import QtWidgets
import db

db.init()
app = QtWidgets.QApplication(sys.argv)
window = mainwindow()
window.show()
sys.exit(app.exec_())
