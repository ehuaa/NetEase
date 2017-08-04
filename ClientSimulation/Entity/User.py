import sqlite3


class User(object):
    def __init__(self, host, username, client_hid):
        super(User, self).__init__()
        self.client_hid = client_hid
        self.username = username
        self.host = host

    def save_info_to_database(self):
        # ***************************************************
        # Not implemented no extra user data
        # ****************************************************
        pass

