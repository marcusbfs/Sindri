# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\dbgui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_databaseWindow(object):
    def setupUi(self, databaseWindow):
        databaseWindow.setObjectName("databaseWindow")
        databaseWindow.setWindowModality(QtCore.Qt.WindowModal)
        databaseWindow.setEnabled(True)
        databaseWindow.resize(997, 640)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(databaseWindow)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_search = QtWidgets.QPushButton(databaseWindow)
        self.btn_search.setObjectName("btn_search")
        self.verticalLayout.addWidget(self.btn_search)
        self.pushButton_4 = QtWidgets.QPushButton(databaseWindow)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.le_db_search = QtWidgets.QLineEdit(databaseWindow)
        self.le_db_search.setObjectName("le_db_search")
        self.horizontalLayout.addWidget(self.le_db_search)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(databaseWindow)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(databaseWindow)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(databaseWindow)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.btn_save_db = QtWidgets.QPushButton(databaseWindow)
        self.btn_save_db.setObjectName("btn_save_db")
        self.verticalLayout_2.addWidget(self.btn_save_db)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.tableWidget_db = QtWidgets.QTableWidget(databaseWindow)
        self.tableWidget_db.setEnabled(True)
        self.tableWidget_db.setAlternatingRowColors(True)
        self.tableWidget_db.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_db.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_db.setShowGrid(True)
        self.tableWidget_db.setWordWrap(True)
        self.tableWidget_db.setCornerButtonEnabled(True)
        self.tableWidget_db.setRowCount(15)
        self.tableWidget_db.setColumnCount(27)
        self.tableWidget_db.setObjectName("tableWidget_db")
        self.tableWidget_db.horizontalHeader().setVisible(True)
        self.tableWidget_db.horizontalHeader().setHighlightSections(True)
        self.tableWidget_db.verticalHeader().setVisible(True)
        self.verticalLayout_3.addWidget(self.tableWidget_db)

        self.retranslateUi(databaseWindow)
        self.pushButton.clicked.connect(databaseWindow.add_substance)
        self.pushButton_2.clicked.connect(databaseWindow.edit_substance)
        self.le_db_search.returnPressed.connect(self.btn_search.click)
        self.pushButton_3.clicked.connect(databaseWindow.del_substance)
        self.btn_search.clicked.connect(databaseWindow.search_substance)
        self.pushButton_4.clicked.connect(databaseWindow.clear_search)
        self.btn_save_db.clicked.connect(databaseWindow.save_db)
        self.le_db_search.textChanged['QString'].connect(databaseWindow.search_substance)
        QtCore.QMetaObject.connectSlotsByName(databaseWindow)

    def retranslateUi(self, databaseWindow):
        _translate = QtCore.QCoreApplication.translate
        databaseWindow.setWindowTitle(_translate("databaseWindow", "Database"))
        self.btn_search.setText(_translate("databaseWindow", "Search"))
        self.pushButton_4.setText(_translate("databaseWindow", "Clear"))
        self.pushButton.setText(_translate("databaseWindow", "Add substance"))
        self.pushButton_2.setText(_translate("databaseWindow", "Edit substance"))
        self.pushButton_3.setText(_translate("databaseWindow", "Delete substance"))
        self.btn_save_db.setText(_translate("databaseWindow", "Save database"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    databaseWindow = QtWidgets.QWidget()
    ui = Ui_databaseWindow()
    ui.setupUi(databaseWindow)
    databaseWindow.show()
    sys.exit(app.exec_())

