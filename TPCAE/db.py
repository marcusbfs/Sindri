import sqlite3

# def init():
#
#     global database_file
#     global db
#     global cursor
#
#     database_file = "db/database.db"
#     db = sqlite3.connect(database_file)
#     cursor = db.cursor()


def init():
    global database_file
    global db
    global cursor

    database_file = "db/database.db"
    db = sqlite3.connect(database_file)
    cursor = db.cursor()

    # def query(command, arguments=[]):
    #     _db = sqlite3.connect(database_file)
    #     _c = _db.cursor()
    #     _c.execute(command, arguments)
    #     results = _c.fetchall()
    #     return results



