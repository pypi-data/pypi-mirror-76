
import sys
import sqlite3

sys.path.append('./')

class DBCreate:
    def __init__(self, dbpath):
        self.conn = sqlite3.connect(dbpath)
        self.cur = self.conn.cursor()

    def CreateTB(self, sql):
        if sql:
            self.cur.execute(sql)

    def CloseCur(self):
        if self.cur:
            self.cur.close()

    def CloseConn(self):
        self.conn.close()




if __name__ == "__main__":
    
    str1 = ""
    db = DBCreate("")

    sql = 'create table weighttb(fid varchar(36), fname varchar(50), weight float)'

    db.CreateTB(sql)

    db.CloseCur()
    db.CloseConn()
