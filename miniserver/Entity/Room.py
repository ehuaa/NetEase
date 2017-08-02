from Arena import Arena
from Services.ArenaServices import ArenaServices
from common import conf
from common.dispatcher import Dispatcher
from common.events import MsgSCStartGame


class Room(object):
    def __init__(self, rid, host, arena_conf_module_name='Configuration.ArenaConf',player_conf_filename='Configuration.PlayerConf'):
        super(Room, self).__init__()
        self.rid = rid
        self.host = host
        self.arena = None

        self.users = {}
        self.owner_id = None
        # Generate dispatcher
        self.dispatcher = Dispatcher()

        # Configuration file
        self.arena_conf_module_name = arena_conf_module_name
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

        self.arena = Arena(self.host, self.arena_conf_module_name, self.player_conf_filename)

        self.register_dispatcher_services()

        self.generate_msg_dict()

        # Send start game message to user
        data = MsgSCStartGame().marshal()
        for hid in self.users.iterkeys():
            self.host.sendClient(hid, data)

        self.arena.start_game(self.users)

    def add_user(self, user):
        # can't add user when game is running
        if self.arena and self.arena.is_game_start and not self.arena.is_game_stop:
            print "Room add user fail"
            return False

        if self.owner_id is None:
            self.owner_id = user.client_hid
            print "Room owner_id set success"
        self.users[user.client_hid] = user
        return True

    def remove_user(self, user):
        if self.arena is not None and self.arena.is_game_start and not self.arena.is_game_stop:
            if len(self.users) == 1:
                self.arena.stop_game()
            else:
                self.arena.player_leave(user.client_hid)
        if user.client_hid in self.users:
            del self.users[user.client_hid]