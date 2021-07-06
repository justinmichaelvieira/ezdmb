import json
import sqlite3


class SqliteImporter:
    def ImportMenuToSqliteFromFile(self, menuFile):
        menuData = json.load(menuFile)
        conn = sqlite3.connect("dmb.db")
        c = conn.cursor()
        c.execute("DELETE FROM menu_item")
        c.execute("VACUUM")
        for mItem in menuData:
            c.execute("INSERT INTO menu_item VALUES(?,?)", (mItem.name, mItem.price))
        c.close()
        conn.close()
        return menuData
