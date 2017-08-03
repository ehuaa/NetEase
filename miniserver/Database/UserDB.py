import sqlite3
class UserInfo(object):
    def __init__(self,username, password):
        super(UserInfo, self).__init__()
        self.username = username
        self.password = password

class UserDB(object):
    def __init__(self, connect, user_table_name="UserAccount"):
        super(UserDB, self).__init__()
        self.connect = connect
        self.user_table_name = user_table_name

        self.check_and_create_user_table()

    def check_and_create_user_table(self):
        c = self.connect.cursor()
        try:
            # try to create the user_login table
            sqlcmd = "CREATE TABLE " + self.user_table_name + \
                     " (username TEXT PRIMARY KEY, password TEXT)"
            c.execute(sqlcmd)
            self.connect.commit()
            # user account table successfully created
        except sqlite3.OperationalError:
            pass
            # user login table already exist

    def add_user_info(self, user_info):
        import hashlib
        c = self.connect.cursor()
        encrypt_password = hashlib.sha256(user_info.password).hexdigest()
        try:
            sqlcmd = "INSERT INTO " + self.user_table_name + \
                     " VALUES (?, ?)"
            c.execute(sqlcmd, (user_info.username, encrypt_password))
            self.connect.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # user already exist

    def user_authentication(self, username, password):
        import hashlib
        encrypt_password = hashlib.sha256(password).hexdigest()
        c = self.connect.cursor()
        sqlcmd = "SELECT * FROM "+self.user_table_name+" WHERE username=?"
        c.execute(sqlcmd, (username,))
        res = c.fetchone()
        error_msg = None
        if res is None:
            error_msg = "User %s doesn't exist.\n" % username
        elif str(res[1]) != encrypt_password:
            error_msg = "Invalid password.\n"

        return error_msg, res