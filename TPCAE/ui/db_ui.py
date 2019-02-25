# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/db_ui.ui',
# licensing of 'designer/db_ui.ui' applies.
#
# Created: Sun Feb 24 20:59:33 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_databaseWindow(object):
    def setupUi(self, databaseWindow):
        databaseWindow.setObjectName("databaseWindow")
        databaseWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        databaseWindow.setEnabled(True)
        databaseWindow.resize(778, 469)
        self.gridLayout = QtWidgets.QGridLayout(databaseWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(databaseWindow)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 758, 449))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_search = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_search.setObjectName("btn_search")
        self.verticalLayout.addWidget(self.btn_search)
        self.pushButton_4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.le_db_search = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.le_db_search.setObjectName("le_db_search")
        self.horizontalLayout.addWidget(self.le_db_search)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_save_db = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_save_db.setObjectName("btn_save_db")
        self.horizontalLayout_3.addWidget(self.btn_save_db)
        self.pushButton_5 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_3.addWidget(self.pushButton_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.tableWidget_db = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget_db.setEnabled(True)
        self.tableWidget_db.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_db.setAlternatingRowColors(True)
        self.tableWidget_db.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.tableWidget_db.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_db.setShowGrid(True)
        self.tableWidget_db.setWordWrap(True)
        self.tableWidget_db.setCornerButtonEnabled(True)
        self.tableWidget_db.setRowCount(0)
        self.tableWidget_db.setColumnCount(27)
        self.tableWidget_db.setObjectName("tableWidget_db")
        self.tableWidget_db.setColumnCount(27)
        self.tableWidget_db.setRowCount(0)
        self.tableWidget_db.horizontalHeader().setVisible(True)
        self.tableWidget_db.horizontalHeader().setHighlightSections(True)
        self.tableWidget_db.verticalHeader().setVisible(True)
        self.verticalLayout_3.addWidget(self.tableWidget_db)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(databaseWindow)
        QtCore.QObject.connect(
            self.pushButton, QtCore.SIGNAL("clicked()"), databaseWindow.add_substance
        )
        QtCore.QObject.connect(
            self.pushButton_2, QtCore.SIGNAL("clicked()"), databaseWindow.edit_substance
        )
        QtCore.QObject.connect(
            self.le_db_search, QtCore.SIGNAL("returnPressed()"), self.btn_search.click
        )
        QtCore.QObject.connect(
            self.pushButton_3, QtCore.SIGNAL("clicked()"), databaseWindow.del_substance
        )
        QtCore.QObject.connect(
            self.btn_search, QtCore.SIGNAL("clicked()"), databaseWindow.search_substance
        )
        QtCore.QObject.connect(
            self.pushButton_4, QtCore.SIGNAL("clicked()"), databaseWindow.clear_search
        )
        QtCore.QObject.connect(
            self.btn_save_db, QtCore.SIGNAL("clicked()"), databaseWindow.save_db
        )
        QtCore.QObject.connect(
            self.le_db_search,
            QtCore.SIGNAL("textChanged(QString)"),
            databaseWindow.search_substance,
        )
        QtCore.QObject.connect(
            self.pushButton_5,
            QtCore.SIGNAL("clicked()"),
            databaseWindow.restore_original_database,
        )
        QtCore.QMetaObject.connectSlotsByName(databaseWindow)

    def retranslateUi(self, databaseWindow):
        databaseWindow.setWindowTitle(
            QtWidgets.QApplication.translate("databaseWindow", "Database", None, -1)
        )
        self.btn_search.setText(
            QtWidgets.QApplication.translate("databaseWindow", "Search", None, -1)
        )
        self.pushButton_4.setText(
            QtWidgets.QApplication.translate("databaseWindow", "Clear", None, -1)
        )
        self.pushButton_4.setShortcut(
            QtWidgets.QApplication.translate("databaseWindow", "Esc", None, -1)
        )
        self.pushButton.setText(
            QtWidgets.QApplication.translate(
                "databaseWindow", "Add substance", None, -1
            )
        )
        self.pushButton_2.setText(
            QtWidgets.QApplication.translate(
                "databaseWindow", "Edit substance", None, -1
            )
        )
        self.pushButton_3.setText(
            QtWidgets.QApplication.translate(
                "databaseWindow", "Delete substance", None, -1
            )
        )
        self.btn_save_db.setText(
            QtWidgets.QApplication.translate(
                "databaseWindow", "Save database", None, -1
            )
        )
        self.pushButton_5.setText(
            QtWidgets.QApplication.translate(
                "databaseWindow", "Restore original database", None, -1
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    databaseWindow = QtWidgets.QWidget()
    ui = Ui_databaseWindow()
    ui.setupUi(databaseWindow)
    databaseWindow.show()
    sys.exit(app.exec_())
