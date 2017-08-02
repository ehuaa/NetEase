import importlib
from copy import deepcopy
from common.timer import TimerManager

class Arena(object):
    def __init__(self, host, arena_conf_filename, player_conf_filename):
        super(Arena, self).__init__()
        self.host = host
        self.player_map = {}
        self.timeManager = TimerManager()
        self.users = None

        # arena configuration
        self.arena_conf = importlib.import_module(arena_conf_filename).configuration
        self.player_conf = importlib.import_module(player_conf_filename).configuration

        # game status
        self.is_game_start = False
        self.is_game_stop = False

    def start_game(self, users):
        from Player import Player
        self.users = users

        # Create player for scene
        born_position = deepcopy(self.arena_conf['player_test_position'])
        born_rotation = deepcopy(self.arena_conf['player_test_rotation'])

        for hid, user in users.iteritems():
            player = Player(hid, user.username, born_position,
                            born_rotation, self.player_conf)
            self.player_map[hid] = player

        # Send player born message
        self.send_player_born_msg()

        # game start
        self.is_game_start = True

    def stop_game(self):
        for player in self.player_map.itervalues():
            if player is not None:
                self.player_leave(player.client_hid)
        self.player_map.clear()
        self.is_game_stop = True

    def tick(self):
        if self.is_game_start and not self.is_game_stop:
            self.timeManager.scheduler()

    def broadcast(self, msg, not_send=None):
        for player in self.player_map.itervalues():
            if player is None:
                continue
            if not player == not_send:
                self.host.sendClient(player.client_hid, msg.marshal())

    def win_game(self):
        from common.events import MsgSCGameWin
        self.broadcast(MsgSCGameWin())
        self.stop_game()

    def lose_game(self):
        from common.events import MsgSCGameOver
        self.broadcast(MsgSCGameOver())
        self.stop_game()

    def player_leave(self, client_hid):
        if not self.is_game_start:
            print "Error player leave: game not start"
            return
        if client_hid not in self.player_map:
            print "Error player leave: player id not in map"
            return
        if client_hid not in self.users:
            print "Error player leave, id not in users"
            return
        player = self.player_map[client_hid]
        user = self.users[client_hid]
        user.save_info_to_database()
        player.set_leave_scene()

    def send_player_born_msg(self):
        for player in self.player_map.itervalues():
            msg = player.generate_born_msg(0)
            self.host.sendClient(player.client_hid, msg.marshal())
            msg = player.generate_born_msg(1)  # send to others
            self.broadcast(msg, not_send=player)

    def handle_player_move(self, msg, client_hid):
        if client_hid not in self.player_map:
            return
        player = self.player_map[client_hid]
        if player.is_dead():
            return
        new_pos = [msg.px, msg.py, msg.pz]

        player.update_position(new_pos)

        # broadcast move info to other player
        self.broadcast(msg, not_send=player)
