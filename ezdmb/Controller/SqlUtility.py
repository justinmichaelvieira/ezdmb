import apsw


class SqlUtility:
    def __init__(self):
        self.dbConn = apsw.Connection("o.db")
        self.cursor = self.dbConn.cursor()
