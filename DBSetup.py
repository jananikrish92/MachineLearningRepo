import sqlite3

class DatabaseManager(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def query(self, arg):
        self.cur.execute(arg)
        return self.cur

    def selectQuery(self, arg,arg1):
        self.cur.execute(arg,arg1)
        return self.cur


    def insertQuery(self,arg, arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10):
        self.cur.execute(arg,(arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10))
        return self.cur

    def insertQuery1(self,arg, arg1,arg2,arg3,arg4):
        self.cur.execute(arg,(arg1,arg2,arg3,arg4))
        return self.cur

    def commitQuery(self):
        self.conn.commit()
      
    def insertQueryProduct(self,arg,arg1,arg2):
        self.cur.execute(arg,(arg1,arg2))
        return self.cur

    def insertQueryProductSimilarity(self,arg,arg1,arg2,arg3):
        self.cur.execute(arg,(arg1,arg2,arg3))
        return self.cur

    def __del__(self):
        self.conn.close()

