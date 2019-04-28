from Views.AddAliasView import AddAliasView
import db


class AddAliasController:
    def __init__(self, edit_db):
        self.edit_db = edit_db
        self.substance_id = self.edit_db.substance_id_int
        self.view = AddAliasView(self)

    def createView(self):
        self.view.le_alias.setFocus()
        self.view.show()

    def ok_clicked(self):
        alias = self.view.le_alias.text()
        if alias != "":
            query = """INSERT INTO substance_name_aliases VALUES(?,?)"""
            db.cursor.execute(query, (self.substance_id, alias))
            self.edit_db.loadAliases()
            self.edit_db.changes_made = True
        self.view.close()

    def cancel_clicked(self):
        self.view.close()


