from PyQt5 import QtCore, QtGui, QtWidgets
from ui.db_ui import Ui_databaseWindow
import sqlite3
import os.path


class databaseWindow(QtWidgets.QWidget, Ui_databaseWindow):
    def __init__(self, parent=None):
        super(databaseWindow, self).__init__(parent)
        self.setupUi(self)

        self.dbfile = "db/database.db"
        self.col_headers = ["Formula", "Name", "CAS #", "Mol. Wt.", "Tfp [K]", "Tb [K]",
                            "Tc [K]", "Pc [bar]", "Vc [cm3/mol]", "Zc", "Omega", "T range (Cp) [K]",
                            "a0", "a1", "a2", "a3", "a4", "Cp IG", "Cp liq.", "Antoine A",
                            "Antoine B", "Antoine C", "Pvp min [bar]", "Tmin [K]", "Pvp max [bar]", "Tmax [K]"]

        self.tableWidget_db.setHorizontalHeaderLabels(self.col_headers)

        self.load_db()
        self.le_db_search.setFocus()

    def __del__(self):
        self.db.close()

    def load_db(self):
        # Abrir banco de dados
        if os.path.isfile(self.dbfile):
            self.db = sqlite3.connect(self.dbfile)
            self.c = self.db.cursor()
            self.show_full_db()
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Database not found")
            error_dialog.exec_()
            raise Exception("Database not found")

    def show_full_db(self):
        try:
            self.query = "SELECT * FROM database"
            self.c.execute(self.query)
            self.results = self.c.fetchall()
            self.update_table_db(self.results)
        except:
            pass

    def update_table_db(self, results):
        number_cols = len(results[0])

        self.tableWidget_db.setRowCount(0)
        self.tableWidget_db.setColumnCount(number_cols)

        for row_number, row_data in enumerate(results):
            self.tableWidget_db.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.tableWidget_db.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))

    def search_substance(self):
        substance_string_name = str(self.le_db_search.text())
        if substance_string_name == '':
            self.show_full_db()
        else:
            try:
                query = "SELECT * FROM database WHERE Name LIKE '%" + substance_string_name + "%'" + \
                        " OR Formula LIKE '%" + substance_string_name + "%'" + \
                        " OR `CAS #` LIKE '%" + substance_string_name + "%'"
                # print(query)
                self.c.execute(query)
                results = self.c.fetchall()
                self.update_table_db(results)
            except:
                self.tableWidget_db.setRowCount(0)

    def add_substance(self):
        pass

    def edit_substance(self):
        pass

    def del_substance(self):
        row_values = []
        current_row = self.tableWidget_db.currentRow()

        if current_row >= 0:
            for i in range(3):
                item = self.tableWidget_db.item(current_row, i).text()
                row_values.append(item)
            query = "DELETE FROM database WHERE Formula LIKE '%" + row_values[0] + "%'" + \
                    " AND Name LIKE '%" + row_values[1] + "%'" + \
                    " AND `CAS #` LIKE '%" + row_values[2] + "%'"

            choice = QtWidgets.QMessageBox.question(self, "Deleting item",
                                                    "Are you sure you want to delete '" + row_values[1] + "'?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)

            if choice == QtWidgets.QMessageBox.Yes:
                try:
                    self.c.execute(query)
                    self.search_substance()
                except:
                    pass

    def save_db(self):
        choice = QtWidgets.QMessageBox.question(self, "Saving database",
                                                "Are you sure you want to save the database?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            try:
                self.db.commit()
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Database saved")
                msg.setWindowTitle("Confirmation")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()
            except:
                pass

    def clear_search(self):
        self.le_db_search.clear()
        # self.show_full_db()
        self.le_db_search.setFocus()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = databaseWindow()
    ui.show()
    sys.exit(app.exec_())
