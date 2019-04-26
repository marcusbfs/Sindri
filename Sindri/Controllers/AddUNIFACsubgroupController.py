from Views.AddUNIFACsubgroupView import AddUNIFACsubgroupView
from Models.LiquidModel import get_all_id_and_subgroups_formulas
import db


class AddUNIFACsubgroupController:
    def __init__(self, edit_db):

        self.edit_db = edit_db
        self.substance_id = self.edit_db.substance_id_int
        self.addSubgroupView = AddUNIFACsubgroupView(self)
        self.subgroups_dict = get_all_id_and_subgroups_formulas()
        self.subgroups_options = list(self.subgroups_dict.keys())
        self.subgroup = self.subgroups_options[0]
        self.subgroup_id = self.getSubgroupID()
        self.frequency = 1
        self.ok_was_clicked = False

    def createView(self):
        self.addSubgroupView.comboBox_UNIFACsubgroup.addItems(self.subgroups_options)
        self.addSubgroupView.show()

    def ok_clicked(self):
        self.subgroup = self.addSubgroupView.comboBox_UNIFACsubgroup.currentText()
        self.frequency = int(
            self.addSubgroupView.spinBox_UNIFACsubgroup_frequency.value()
        )
        self.subgroup_id = self.getSubgroupID()
        self.ok_was_clicked = True
        query = """INSERT INTO substance_unifac_subgroups (substance_id, subgroup_id,frequency) VALUES (?,?,?)"""
        db.cursor.execute(query, (self.substance_id, self.subgroup_id, self.frequency))
        # db.db.commit()
        self.edit_db.loadUNIFACsubgroups()
        self.addSubgroupView.close()

    def cancel_clicked(self):
        self.ok_was_clicked = False
        self.addSubgroupView.close()

    def getSubgroup(self) -> str:
        return self.subgroup

    def getSubgroupID(self) -> int:
        return self.subgroups_dict[self.getSubgroup()]

    def getFrequency(self) -> int:
        return self.frequency

    def wasOKClicked(self):
        return self.ok_was_clicked
