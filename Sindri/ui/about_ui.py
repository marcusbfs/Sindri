# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/about_ui.ui',
# licensing of 'designer/about_ui.ui' applies.
#
# Created: Thu Apr  4 09:32:01 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_DialogAbout(object):
    def setupUi(self, DialogAbout):
        DialogAbout.setObjectName("DialogAbout")
        DialogAbout.resize(411, 341)
        self.gridLayout = QtWidgets.QGridLayout(DialogAbout)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(DialogAbout)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 391, 321))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowser_About = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser_About.setOpenExternalLinks(True)
        self.textBrowser_About.setObjectName("textBrowser_About")
        self.gridLayout_2.addWidget(self.textBrowser_About, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(DialogAbout)
        QtCore.QMetaObject.connectSlotsByName(DialogAbout)

    def retranslateUi(self, DialogAbout):
        DialogAbout.setWindowTitle(
            QtWidgets.QApplication.translate("DialogAbout", "About", None, -1)
        )
        self.textBrowser_About.setHtml(
            QtWidgets.QApplication.translate(
                "DialogAbout",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;"><br /></p></body></html>',
                None,
                -1,
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    DialogAbout = QtWidgets.QDialog()
    ui = Ui_DialogAbout()
    ui.setupUi(DialogAbout)
    DialogAbout.show()
    sys.exit(app.exec_())
