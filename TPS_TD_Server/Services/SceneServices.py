from common import conf
from common.dispatcher import Service


class SceneServices(Service):
	def __init__(self, host, scene, sid=conf.SCENE_SERVICES):
		super(SceneServices, self).__init__(sid)
		self.host = host
		self.scene = scene

		commands = {
			0: self.player_move,
			1: self.player_normal_attack,
			2: self.player_skill_attack,
			3: self.player_setup_trap,
			4: self.buy_level,
		}
		self.register_commands(commands)

	def player_move(self, msg, client_hid):
		self.scene.handle_player_move(msg, client_hid)

	def player_normal_attack(self, msg, client_hid):
		self.scene.handle_player_normal_attack(msg, client_hid)

	def player_skill_attack(self, msg, client_hid):
		self.scene.handle_player_skill_attack(msg, client_hid)

	def player_setup_trap(self, msg, client_hid):
		self.scene.handle_player_setup_trap(msg, client_hid)

	def buy_level(self, msg, client_hid):
		self.scene.handle_buy_level(msg, client_hid)

