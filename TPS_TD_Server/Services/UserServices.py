import sqlite3

from Entity.Room import Room
from Entity.User import User
from common import conf
from common.dispatcher import Service
from common.events import MsgLoginResult


class UserServices(Service):
    def __init__(self, host, login_user_map, rooms, user_room_map, sid=conf.USER_SERVICES):
        super(UserServices, self).__init__(sid)
        self.host = host
        self.login_user_map = login_user_map
        self.rooms = rooms
        self.user_room_map = user_room_map
        self.username_to_user_map = {}
        commands = {
            0: self.register,
            1: self.login,
            2: self.logout,
            3: self.create_room,
            4: self.join_room,
            5: self.leave_room,
            6: self.start_game,
        }
        self.register_commands(commands)
        # database
        self.conn = None
        self.check_and_create_user_login_table()

    def send_login_result(self, client_hid, msg):
        ok = 0
        if msg == '':
            ok = 1
        msg_login_result = MsgLoginResult(ok, msg)
        self.host.sendClient(client_hid, msg_login_result.marshal())

    def send_room_list_to_login_player(self, client_hid):
        from common.events import MsgRoomList
        s = ""
        for room in self.rooms:
            if room is not None:
                if room.owner_id not in self.login_user_map:
                    # print "send room list error: room.owner_id = ", room.owner_id
                    continue
                s = s + str(room.rid) + ": " + str(self.login_user_map[room.owner_id].username) + ','
        msg = MsgRoomList(s[:-1])
        self.host.sendClient(client_hid, msg.marshal())

    def send_room_list_to_all_players(self):
        from common.events import MsgRoomList
        s = ""
        for room in self.rooms:
            if room is not None:
                if room.owner_id not in self.login_user_map:
                    # print "send room list error: room.owner_id = ", room.owner_id
                    continue
                s = s + str(room.rid) + ": " + str(self.login_user_map[room.owner_id].username) + ','
        msg = MsgRoomList(s[:-1])
        for user in self.login_user_map.itervalues():
            self.host.sendClient(user.client_hid, msg.marshal())

    def get_room_id(self):
        rid = -1
        for i in xrange(len(self.rooms)):
            if self.rooms[i] is None:
                rid = i
                break
        if rid == -1:
            rid = len(self.rooms)
            self.rooms.append(None)
        return rid

    def is_user_login(self, client_hid):
        return client_hid in self.login_user_map

    def start_game(self, msg, client_hid):
        """
		Start game with other players in the room
		"""
        if not self.is_user_login(client_hid):
            print "Start game error: not login"
            return
        if client_hid not in self.user_room_map:
            # single person game
            self.create_room(None, client_hid)
        room = self.user_room_map[client_hid]
        # only the room owner can start game
        if room.owner_id != client_hid:
            print "Start game error: not room owner"
            return
        room.start_game()

    def create_room(self, msg, client_hid):
        """
		Auto generate room id and create a new room
		"""
        if not self.is_user_login(client_hid):
            print "Create room error: user already login"
            return
        if client_hid in self.user_room_map:
            print "Create room error: user already in room"
            return
        rid = self.get_room_id()
        room = Room(rid, self.host)
        print "create room: ", room
        self.rooms[rid] = room
        if room.add_user(self.login_user_map[client_hid]):
            print "room add user success"
            self.user_room_map[client_hid] = room
            self.send_room_list_to_all_players()

    def join_room(self, msg, client_hid):
        """
		User join room
		"""
        if not self.is_user_login(client_hid):
            print "Join room error: not login"
            return
        if client_hid in self.user_room_map:
            print "Join room error: already in room"
            return

        rid = msg.rid
        if not 0 <= rid < len(self.rooms) or self.rooms[rid] is None:
            print "Join room error: room id error"
            return
        if self.rooms[rid].add_user(self.login_user_map[client_hid]):
            self.user_room_map[client_hid] = self.rooms[rid]

    def leave_room(self, msg, client_hid):
        """
		User leave room
		"""
        if not self.is_user_login(client_hid):
            print "Leave room error: not login"
            return

        if client_hid not in self.user_room_map:
            print "Leave room error: not in room"
            return
        print "leave room"
        # leave room
        room = self.user_room_map[client_hid]
        del self.user_room_map[client_hid]
        room.remove_user(self.login_user_map[client_hid])
        # delete room
        if len(room.users) == 0:
            print "delete room"
            self.rooms[room.rid] = None  # rooms is a list
            self.send_room_list_to_all_players()

    def register(self, msg, client_hid):
        """
		Handle user register, auto login if register successful
		"""
        if self.add_user_to_database(msg.username, msg.password):
            self.login(msg, client_hid)
        else:
            self.send_login_result(client_hid, "user %s already exist.\n" % msg.username)

    def login(self, msg, client_hid):
        """
		Handle user login
		"""
        # authentication
        error_msg, res = self.user_authentication(msg.username, msg.password)
        if error_msg:  # login fail
            self.send_login_result(client_hid, error_msg)
            return
        username = msg.username
        # user already login in ?
        if username in self.username_to_user_map:
            print "user login again, kick the old one out"
            # self.send_login_result(client_hid, "%s is already logged in.\n" % username)
            self.logout(None, self.username_to_user_map[username].client_hid)

        self.send_login_result(client_hid, '')
        # valid user
        user = User(username, client_hid, res[2], res[3])
        self.username_to_user_map[username] = user
        self.login_user_map[client_hid] = user
        self.send_room_list_to_login_player(client_hid)

    def logout(self, msg, client_hid):
        if client_hid not in self.login_user_map:
            return
        print "logout"
        if client_hid in self.user_room_map:
            self.leave_room(None, client_hid)
        # clear login info
        del self.username_to_user_map[self.login_user_map[client_hid].username]
        del self.login_user_map[client_hid]

    def check_and_create_user_login_table(self):
        """
		Create the user login table if it does not exist
		"""
        self.conn = sqlite3.connect(conf.DB_NAME)  # connect to the user information database
        c = self.conn.cursor()
        try:
            # try to create the user_login table
            c.execute(
                "CREATE TABLE UserProperty (username TEXT PRIMARY KEY, password TEXT, skillLevel INTEGER, trapLevel INTEGER)")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass  # user login table already exist

    def add_user_to_database(self, username, password):
        """
		Add a new user into the database
		"""
        import hashlib
        c = self.conn.cursor()
        encrypt_password = hashlib.sha256(password).hexdigest()
        try:
            c.execute("INSERT INTO UserProperty VALUES (?, ?, ?, ?)", (username, encrypt_password, 0, 0))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # user already exist

    def user_authentication(self, username, password):
        """
		Check to see if the user is valid
		"""
        import hashlib
        encrypt_password = hashlib.sha256(password).hexdigest()
        c = self.conn.cursor()
        c.execute("SELECT * FROM UserProperty WHERE username=?", (username,))
        res = c.fetchone()
        error_msg = None
        if res is None:
            error_msg = "User %s doesn't exist.\n" % username
        elif str(res[1]) != encrypt_password:
            error_msg = "Invalid password.\n"
        return error_msg, res
