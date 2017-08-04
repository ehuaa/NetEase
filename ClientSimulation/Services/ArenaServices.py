from common import conf
from common.dispatcher import Service


class ArenaServices(Service):
    def __init__(self, host, arena, sid=conf.ARENA_SERVICES):
        super(ArenaServices, self).__init__(sid)
        self.host = host
        self.arena = arena

        commands = {
            0: self.player_move
        }
        self.register_commands(commands)

    def player_move(self, msg, client_hid):
        self.arena.handle_player_move(msg, client_hid)