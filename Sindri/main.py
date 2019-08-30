import sys

from PySide2 import QtWidgets, QtGui

import db
from mainwindow import mainwindow

db.init()
app = QtWidgets.QApplication(sys.argv)
app.setStyle("fusion")
try:
    # QtGui.QFontDatabase.addApplicationFont("css/font/Azonix.otf")
    with open("css/mainstyle.css", "r") as f_css:
        app.setStyleSheet(f_css.read())
except:
    pass
default_font = QtGui.QFont()
default_font.setPointSize(10)
QtWidgets.QApplication.setFont(default_font)
window = mainwindow()
window.show()
sys.exit(app.exec_())
