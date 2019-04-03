import sys

from PySide2 import QtWidgets

import db
from mainwindow import mainwindow

db.init()
app = QtWidgets.QApplication(sys.argv)
window = mainwindow()
window.show()
sys.exit(app.exec_())
