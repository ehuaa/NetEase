import importlib
from copy import deepcopy
from common.timer import TimerManager

class Arena(object):
    def __init__(self, host, arena_conf_filename, player_conf_filename):
        super(Arena, self).__init__()
        self.host = host
        self.client_id_to_player_map = {}
        self.username_to_user = {}
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
        self.username_to_user = users

        # Create player for scene
        born_position = deepcopy(self.arena_conf['player_test_position'])
        born_rotation = deepcopy(self.arena_conf['player_test_rotation'])

        for hid, user in self.username_to_user.items():
            player = Player(user.client_hid, user.username, born_position,
                            born_rotation, self.player_conf)
            self.client_id_to_player_map[user.client_hid] = player

        # Send player born message
        self.send_player_born_msg()

        # game start
        self.is_game_start = True

    def stop_game(self):
        pass

    def tick(self):
        if self.is_game_start and not self.is_game_stop:
            self.timeManager.scheduler()

    def broadcast(self, msg, not_send=None):
        for player in self.client_id_to_player_map.itervalues():
            if player is None:
                continue
            if not player == not_send:
                self.host.sendClient(player.client_hid, msg.marshal())

    def player_leave(self, client_hid):
        pass

    def send_player_born_msg(self):
        for player in self.client_id_to_player_map.itervalues():
            msg = player.generate_born_msg(0)  # send to itself
            self.host.sendClient(player.client_hid, msg.marshal())
            msg = player.generate_born_msg(1)  # send to others
            self.broadcast(msg, not_send=player)

    def handle_player_move(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        print "Player Move to:%f %f %f",msg.px,msg.py,msg.pz

        new_pos = [msg.px, msg.py, msg.pz]
        player.update_position(new_pos)

        # broadcast move info to other player
        self.broadcast(msg, not_send=player)
