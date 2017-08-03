from Scene import Scene
from Services.SceneServices import SceneServices
from common import conf
from common.dispatcher import Dispatcher
from common.events import MsgStartGame


class Room(object):
    def __init__(self, rid, host, scene_conf_module_name='Configuration.SceneLevelOne',
                 enemy_conf_filename='Configuration.EnemyConf', arrow_conf_filename='Configuration.ArrowConf',
                 trap_conf_filename='Configuration.TrapConf', player_conf_filename='Configuration.PlayerConf'):
        super(Room, self).__init__()
        self.rid = rid
        self.host = host
        self.scene = None
        # configuration
        self.scene_conf_module_name = scene_conf_module_name
        self.enemy_conf_filename = enemy_conf_filename
        self.arrow_conf_filename = arrow_conf_filename
        self.trap_conf_filename = trap_conf_filename
        self.player_conf_filename = player_conf_filename

        self.users = {}
        self.owner_id = None
        # Generate dispatcher
        self.dispatcher = Dispatcher()

        # received message
        self.msg_dict = None

    def generate_msg_dict(self):
        """
		Map msg_type to message object
		"""
        from common.events import MsgPlayerMove
        from common.events import MsgPlayerNormalAttack
        from common.events import MsgPlayerSkillAttack
        from common.events import MsgPlayerSetupTrap
        from common.events import MsgBuyLevel
        self.msg_dict = {
            conf.MSG_PLAYER_MOVE: MsgPlayerMove(),
            conf.MSG_PLAYER_NORMAL_ATTACK: MsgPlayerNormalAttack(),
            conf.MSG_PLAYER_SKILL_ATTACK: MsgPlayerSkillAttack(),
            conf.MSG_PLAYER_SETUP_TRAP: MsgPlayerSetupTrap(),
            conf.MSG_BUY_LEVEL: MsgBuyLevel(),
        }

    def register_dispatcher_services(self):
        """
		Register services to dispatcher
		"""
        self.dispatcher.register(conf.SCENE_SERVICES, SceneServices(self.host, self.scene))

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
        if self.scene:
            self.scene.tick()

    def start_game(self):
        """
		Start game
		"""
        # Can't start game when game is running
        if self.scene and self.scene.is_game_start and not self.scene.is_game_stop:
            return False

        self.scene = Scene(self.host, self.scene_conf_module_name, self.enemy_conf_filename,
                           self.arrow_conf_filename, self.trap_conf_filename, self.player_conf_filename)

        self.register_dispatcher_services()

        self.generate_msg_dict()

        # Send start game message to user
        data = MsgStartGame().marshal()
        for hid in self.users.iterkeys():
            self.host.sendClient(hid, data)

        self.scene.start_game(self.users)

    def add_user(self, user):
        # can't add user when game is running
        if self.scene and self.scene.is_game_start and not self.scene.is_game_stop:
            print "Room add user fail"
            return False

        if self.owner_id is None:
            self.owner_id = user.client_hid
            print "Room owner_id set success"
        self.users[user.client_hid] = user
        return True

    def remove_user(self, user):
        if self.scene is not None and self.scene.is_game_start and not self.scene.is_game_stop:
            if len(self.users) == 1:
                self.scene.stop_game()
            else:
                self.scene.player_leave(user.client_hid)
        if user.client_hid in self.users:
            del self.users[user.client_hid]
