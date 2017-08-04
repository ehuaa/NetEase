from UserDB import UserDB
import sqlite3

class DBManager(object):
    def __init__(self, db_name, dbconf=None):
        super(DBManager, self).__init__()
        self.db_name = db_name
        self.user_db = None

        with sqlite3.connect(self.db_name) as self.connect:
            self.cursor = self.connect.cursor()
            self.user_db = UserDB(self.connect)
            # other database manager

    # Close the db cursor
    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()