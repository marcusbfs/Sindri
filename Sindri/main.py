import sys

from PySide2 import QtWidgets, QtGui

import db
from mainwindow import mainwindow

db.init()
app = QtWidgets.QApplication(sys.argv)
app.setStyle("fusion")
try:
    QtGui.QFontDatabase.addApplicationFont("css/font/Azonix.otf")
    with open("css/mainstyle.css", "r") as f_css:
        app.setStyleSheet(f_css.read())
except:
    pass
window = mainwindow()
window.show()
sys.exit(app.exec_())
