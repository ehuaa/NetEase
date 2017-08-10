from Arena import Arena
from Services.ArenaServices import ArenaServices
from common import conf
from common.dispatcher import Dispatcher
from common.events import MsgSCStartGame,MsgSCRoommateAdd,MsgSCRoommateDel


class Room(object):

    def __init__(self, rid, host, max_user_num = 2,arena_conf_filename='Configuration.ArenaConf', player_conf_filename='Configuration.PlayerConf'):
        super(Room, self).__init__()
        self.rid = rid
        self.host = host
        self.arena = None

        self.max_user_num = max_user_num
        self.username_to_user_map = {}

        # Generate dispatcher
        self.dispatcher = Dispatcher()

        # Configuration file
        self.arena_conf_filename = arena_conf_filename
        self.player_conf_filename = player_conf_filename

        # received message
        self.msg_dict = None

    def generate_msg_dict(self):
        from common.events import MsgCSPlayerMove
        self.msg_dict = {
            conf.MSG_CS_PLAYER_MOVE: MsgCSPlayerMove()
        }

    def register_dispatcher_services(self):
        self.dispatcher.register(conf.ARENA_SERVICES, ArenaServices(self.host, self.arena))

    def dispatch(self, msg, client_hid):
        self.dispatcher.dispatch(msg, client_hid)

    def handle_received_msg(self, msg_type, data, client_hid):
        if msg_type in self.msg_dict:
            msg = self.msg_dict[msg_type]
            msg.unmarshal(data)
            self.dispatcher.dispatch(msg, client_hid)
        else:
            print "Can't handle received message in room"

    def tick(self):
        if self.arena:
            self.arena.tick()

    def start_game(self):
        # Can't start game when game is running
        if self.arena and self.arena.is_game_start and not self.arena.is_game_stop:
            return False

        self.arena = Arena(self.host, self.arena_conf_filename, self.player_conf_filename)

        self.register_dispatcher_services()

        self.generate_msg_dict()

        # Send start game message to all roommates
        data = MsgSCStartGame().marshal()
        for k,v in self.username_to_user_map.items():
            self.host.sendClient(v.client_hid, data)

        self.arena.start_game(self.username_to_user_map)

    def add_user(self, user):
        if self.username_to_user_map.has_key(user.username) == False and\
                        len(self.username_to_user_map) >= self.max_user_num:
            return False   # room is full

        # user back again
        if self.arena and self.arena.is_game_start and not self.arena.is_game_stop:
            self.arena.player_enter_again(user)
            return True

        self.username_to_user_map[user.username] = user
        self.broadcast_roommate_add(user.username)

        if len(self.username_to_user_map) >= self.max_user_num:
            self.start_game()

        return True

    def remove_user(self, user):
        if self.username_to_user_map.has_key(user.username) is False:
            return False   # user not find

        if self.arena and self.arena.is_game_start and not self.arena.is_game_stop:
            self.arena.player_leave(user.client_hid)
        else:
            del self.username_to_user_map[user.username]
            self.broadcast_roommate_del(user.username)
            if len(self.username_to_user_map) <= 0:
                return True

        return False

    def broadcast_roommate_add(self, username):
        msg = MsgSCRoommateAdd(username)
        data = msg.marshal()

        for username, user in self.username_to_user_map.items():
            self.host.sendClient(user.client_hid, data)

    def broadcast_roommate_del(self, username):
        msg = MsgSCRoommateDel(username)
        data = msg.marshal()

        for username, user in self.username_to_user_map.items():
            self.host.sendClient(user.client_hid, data)

    # game over return True else False
    def is_valid(self):
        if self.arena and self.arena.is_game_stop:
            return False
        else:
            return True

