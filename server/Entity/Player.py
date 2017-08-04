from common.events import MsgSCPlayerBorn

class Player(object):
    def __init__(self, client_hid, name, position, rotation, player_conf):
        super(Player, self).__init__()
        self.client_hid = client_hid
        self.name = name
        self.is_leave_scene = False

        self.speed = player_conf['move_speed']

        # basic properties
        self.health = 100

        # scene info
        self.position = position
        self.rotation = rotation

    def generate_born_msg(self, send_to_others):
        return MsgSCPlayerBorn(self.client_hid, send_to_others, self.name,self.health, self.position[0], self.position[1], self.position[2],self.rotation[0],self.rotation[1], self.rotation[2])

    def set_leave_scene(self):
        self.is_leave_scene = True

    def is_dead(self):
        if self.is_leave_scene:
            return True
        return self.health <= 0

    def update_position(self, pos):
        if self.is_dead():
            return
        self.position[0] = pos[0]
        self.position[1] = pos[1]
        self.position[2] = pos[2]