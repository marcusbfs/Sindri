import sys
from mainwindow import mainwindow
from PySide2 import QtWidgets
import db

db.init()
app = QtWidgets.QApplication(sys.argv)
window = mainwindow()
window.show()
sys.exit(app.exec_())
