import sqlite3

class DBHelper:

    def __init__(self, dbname="todolist.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        print("Creating table")
        tblstmt = "CREATE TABLE IF NOT EXISTS todo (description text, owner text)"
        itemIndex = "CREATE INDEX IF NOT EXISTS todoIndex ON todo (description ASC)"
        ownIndex = "CREATE INDEX IF NOT EXISTS ownIndex ON todo (owner ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(itemIndex)
        self.conn.execute(ownIndex)
        self.conn.commit()

    def addItem(self, item_text, owner):
        stmt = "INSERT INTO todo (description, owner) VALUES (?, ?)"
        args = (item_text, owner, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def deleteItem(self, item_text, owner):
        stmt = "DELETE FROM todo WHERE description = (?) AND owner = (?)"
        args = (item_text, owner, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def getItems(self, owner):
        stmt = "SELECT description FROM todo WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]
