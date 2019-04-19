from PySide2 import QtCore, QtGui, QtWidgets

from ui.about_ui import Ui_DialogAbout
from _devinfo import __SOFTWARE_NAME__


class Window_About(QtWidgets.QDialog, Ui_DialogAbout):
    def __init__(self, parent=None):
        super(Window_About, self).__init__(parent)
        self.setupUi(self)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.setWindowTitle("About {}".format(__SOFTWARE_NAME__))

        self.abouthtml = "texts/about.html"

        with open(self.abouthtml, "r") as aboutContent:
            self.textBrowser_About.setHtml(aboutContent.read())
