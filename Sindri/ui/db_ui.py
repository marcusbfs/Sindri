# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/db_ui.ui',
# licensing of 'designer/db_ui.ui' applies.
#
# Created: Fri Apr 19 13:26:35 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_databaseWindow(object):
    def setupUi(self, databaseWindow):
        databaseWindow.setObjectName("databaseWindow")
        databaseWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        databaseWindow.setEnabled(True)
        databaseWindow.resize(744, 398)
        databaseWindow.setMinimumSize(QtCore.QSize(600, 250))
        databaseWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout = QtWidgets.QGridLayout(databaseWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(databaseWindow)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 724, 378))
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
        self.btn_clearSearch = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_clearSearch.setObjectName("btn_clearSearch")
        self.verticalLayout.addWidget(self.btn_clearSearch)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.le_db_search = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.le_db_search.setObjectName("le_db_search")
        self.horizontalLayout.addWidget(self.le_db_search)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_addSubstance = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_addSubstance.setObjectName("btn_addSubstance")
        self.horizontalLayout_2.addWidget(self.btn_addSubstance)
        self.btn_editSubstance = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_editSubstance.setObjectName("btn_editSubstance")
        self.horizontalLayout_2.addWidget(self.btn_editSubstance)
        self.btn_deleteSubstance = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_deleteSubstance.setObjectName("btn_deleteSubstance")
        self.horizontalLayout_2.addWidget(self.btn_deleteSubstance)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_save_db = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_save_db.setObjectName("btn_save_db")
        self.horizontalLayout_3.addWidget(self.btn_save_db)
        self.btn_RestoreOriginalDB = QtWidgets.QPushButton(
            self.scrollAreaWidgetContents
        )
        self.btn_RestoreOriginalDB.setObjectName("btn_RestoreOriginalDB")
        self.horizontalLayout_3.addWidget(self.btn_RestoreOriginalDB)
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
        self.tableWidget_db.setColumnCount(26)
        self.tableWidget_db.setObjectName("tableWidget_db")
        self.tableWidget_db.setColumnCount(26)
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
            self.btn_addSubstance,
            QtCore.SIGNAL("clicked()"),
            databaseWindow.add_substance,
        )
        QtCore.QObject.connect(
            self.btn_editSubstance,
            QtCore.SIGNAL("clicked()"),
            databaseWindow.edit_substance,
        )
        QtCore.QObject.connect(
            self.le_db_search, QtCore.SIGNAL("returnPressed()"), self.btn_search.click
        )
        QtCore.QObject.connect(
            self.btn_deleteSubstance,
            QtCore.SIGNAL("clicked()"),
            databaseWindow.del_substance,
        )
        QtCore.QObject.connect(
            self.btn_search, QtCore.SIGNAL("clicked()"), databaseWindow.search_substance
        )
        QtCore.QObject.connect(
            self.btn_clearSearch,
            QtCore.SIGNAL("clicked()"),
            databaseWindow.clear_search,
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
            self.btn_RestoreOriginalDB,
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
        self.btn_clearSearch.setText(
            QtWidgets.QApplication.translate("databaseWindow", "Clear", None, -1)
        )
        self.btn_clearSearch.setShortcut(
            QtWidgets.QApplication.translate("databaseWindow", "Esc", None, -1)
        )
        self.btn_addSubstance.setText(
            QtWidgets.QApplication.translate(
                "databaseWindow", "Add substance", None, -1
            )
        )
        self.btn_editSubstance.setText(
            QtWidgets.QApplication.translate(
                "databaseWindow", "Edit substance", None, -1
            )
        )
        self.btn_deleteSubstance.setText(
            QtWidgets.QApplication.translate(
                "databaseWindow", "Delete substance", None, -1
            )
        )
        self.btn_save_db.setText(
            QtWidgets.QApplication.translate(
                "databaseWindow", "Save database", None, -1
            )
        )
        self.btn_RestoreOriginalDB.setText(
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
