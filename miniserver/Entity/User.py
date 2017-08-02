import sqlite3


class User(object):
    def __init__(self, username, test_data, client_hid):
        super(User, self).__init__()
        self.username = username
        self.rid = None
        self.client_hid = client_hid
        self.test_data = test_data

    def save_info_to_database(self):
        from common import conf
        conn = sqlite3.connect(conf.DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE UserProperty SET nick_name=? WHERE username=?",
                  (self.test_data, self.username))
        conn.commit()