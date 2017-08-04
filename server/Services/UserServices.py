from Entity.User import User
from common import conf
from common.dispatcher import Service
from common.events import MsgSCLoginResult


class UserServices(Service):
    def __init__(self, host, sid=conf.USER_SERVICES):
        super(UserServices, self).__init__(sid)
        self.host = host

        self.client_hid_to_user_map = {}
        self.username_to_user_map = {}

        commands = {
            0: self.register,
            1: self.login,
            2: self.logout
        }
        self.register_commands(commands)

    def send_login_result(self, client_hid, msg):
        ok = 0
        if msg == '':
            ok = 1
        msg_login_result = MsgSCLoginResult(ok, msg)
        self.host.sendClient(client_hid, msg_login_result.marshal())

    def is_user_login(self, client_hid):
        return client_hid in self.client_hid_to_user_map

    def register(self, msg, client_hid):
        if self.add_user_to_database(msg.username, msg.password):
            self.login(msg, client_hid)
        else:
            self.send_login_result(client_hid, "user %s already exist.\n" % msg.username)

    def login(self, msg, client_hid):
        # authentication
        error_msg, res = self.user_authentication(msg.username, msg.password)
        if error_msg:  # login fail
            self.send_login_result(client_hid, error_msg)
            return
        username = msg.username

        # user already login in ?
        if username in self.username_to_user_map:
            # "user login again, kick the old one out"
            self.logout(self.username_to_user_map[username].client_hid)

        self.send_login_result(client_hid, '')
        # valid user
        user = User(self.host, username, client_hid)
        self.username_to_user_map[username] = user
        self.client_hid_to_user_map[client_hid] = user

        self.host.room_manager.add_user(user)

    def logout(self, client_hid):
        if client_hid not in self.client_hid_to_user_map:
            return
        print "logout"

        # Remove it from the room
        user = User(self.host, self.client_hid_to_user_map[client_hid].username, client_hid)
        self.host.room_manager.remove_user(user)

        del self.username_to_user_map[self.client_hid_to_user_map[client_hid].username]
        del self.client_hid_to_user_map[client_hid]

    def add_user_to_database(self, username, password):
        return self.host.db_manager.add_user_info(username, password)

    def user_authentication(self, username, password):
        return self.host.db_manager.user_db.user_authentication(username, password)
