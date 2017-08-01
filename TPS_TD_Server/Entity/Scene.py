import importlib
import time
from copy import deepcopy
from Enemy import Enemy
from common.timer import TimerManager


class Scene(object):
    def __init__(self, host, scene_conf_filename, enemy_conf_filename, arrow_conf_filename,
                 trap_conf_filename, player_conf_filename):
        super(Scene, self).__init__()
        self.host = host
        self.player_map = {}
        self.escape_enemies_num = 0
        self.timeManager = TimerManager()
        self.users = None

        # Scene configuration
        self.scene_conf = importlib.import_module(scene_conf_filename).configuration
        self.enemy_conf = importlib.import_module(enemy_conf_filename).configuration
        self.arrow_conf = importlib.import_module(arrow_conf_filename).configuration
        self.trap_conf = importlib.import_module(trap_conf_filename).configuration
        self.player_conf = importlib.import_module(player_conf_filename).configuration

        # Scene settings
        self.scene_grid = []
        self.enemy_spawn_time = self.scene_conf['enemy_spawn_time']
        self.max_escape_enemies_num = self.scene_conf['max_escape_enemies_num']
        # Enemy move speed
        self.enemy_move_speed = self.scene_conf['enemy_move_speed']
        self.enemy_escape_range = self.scene_conf['enemy_escape_range']

        # spawn time record
        self.last_group_end_time = None
        self.spawn_group_id = 0
        self.already_spawn_count = 0
        self.group_enemy_dead_escape_num = 0
        self.enemy_groups = self.scene_conf['enemy_group_num']

        # game status
        self.is_game_start = False
        self.is_game_stop = False

        # entities
        self.enemy_count = 0
        self.enemies = {}
        self.arrow_count = 0
        self.arrows = {}
        self.trap_count = 0
        self.traps = {}

        self.enemy_bullets = {}

    def start_game(self, users):
        from Player import Player
        self.users = users

        # load scene grid
        self.load_scene_map_grid(self.scene_conf['scene_map_filename'])

        # Create player for scene
        born_positions = deepcopy(self.scene_conf['player_born_positions'])
        born_rotation = deepcopy(self.scene_conf['player_born_rotation'])
        idx = 0
        for hid, user in users.iteritems():
            player = Player(hid, user.username, user.skill_level, user.trap_level, born_positions[idx],
                            born_rotation, self.player_conf)
            self.player_map[hid] = player
            idx += 1
            if idx == len(born_positions):  # the rest players born in the last position
                idx -= 1

        # Send player born message
        self.send_player_born_msg()

        # setup time manager
        self.timeManager.add_repeat_timer(self.enemy_spawn_time, self.spawn_one_enemy)
        self.timeManager.add_repeat_timer(1.0 / self.enemy_move_speed, self.update_enemy_behavior)
        self.timeManager.add_repeat_timer(self.scene_conf['arrow_update_time'], self.update_arrows_behavior)
        self.timeManager.add_repeat_timer(self.scene_conf['trap_update_time'], self.update_traps_behavior)
        # game start
        self.is_game_start = True

    def stop_game(self):
        """
		All players leave scenes
		"""
        for player in self.player_map.itervalues():
            if player is not None:
                self.player_leave(player.client_hid)
        self.player_map.clear()
        self.is_game_stop = True

    def tick(self):
        if self.is_game_start and not self.is_game_stop:
            self.timeManager.scheduler()

    def broadcast(self, msg, not_send=None):
        """
		Send message to every player
		"""
        for player in self.player_map.itervalues():
            if player is None:
                continue
            if not player == not_send:
                self.host.sendClient(player.client_hid, msg.marshal())

    def win_game(self):
        from common.events import MsgGameWin
        self.broadcast(MsgGameWin())
        self.stop_game()

    def lose_game(self):
        from common.events import MsgGameOver
        self.broadcast(MsgGameOver())
        self.stop_game()

    def player_leave(self, client_hid):
        """
		Player leave scene
		"""
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
        user.set_info_from_player(player.skill_level, player.trap_level)
        user.save_info_to_database()
        player.set_leave_scene()

    def send_player_born_msg(self):
        """
		Call by start game only once
		"""
        for player in self.player_map.itervalues():
            msg = player.generate_born_msg(0)
            self.host.sendClient(player.client_hid, msg.marshal())
            msg = player.generate_born_msg(1)  # send to others
            self.broadcast(msg, not_send=player)

    def handle_buy_level(self, msg, client_hid):
        if client_hid not in self.player_map:
            return
        player = self.player_map[client_hid]
        msg = player.buy_level(msg.level_type)
        if msg is not None:
            self.host.sendClient(player.client_hid, msg.marshal())
        else:
            print "Buy level fail"

    def update_traps_behavior(self):
        """
		Trap triggers, attack enemies, dead
		"""
        dead_traps = []
        for trap in self.traps.itervalues():
            if trap is None or trap.is_dead():
                self.clear_trap_in_grid(trap.position, trap.configuration)
                dead_traps.append(trap.tid)
                continue
            if trap.try_trigger(self.enemies, self):
                continue
        # delete dead traps
        for tid in dead_traps:
            del self.traps[tid]

    def generate_trap_id(self):
        tid = self.trap_count
        self.trap_count += 1
        self.trap_count = divmod(self.trap_count, self.trap_conf['max_trap_id_num'])[1]
        return tid

    def check_trap_setup_position_legal(self, pos, configuration):
        """
		Check trap position legal
		"""
        bound_len = configuration['attack_size_length'] / 2
        if not bound_len <= pos[0] < len(self.scene_grid) - bound_len:
            return False
        is_collision = False
        for i in xrange(pos[0] - bound_len, pos[0] + bound_len):
            for j in xrange(pos[2] - bound_len, pos[2] + bound_len):
                if self.scene_grid[i][j].value != '.':  # may be '#' or '*'
                    is_collision = True
                    break
        if is_collision:
            return False
        return True

    def clear_trap_in_grid(self, pos, configuration):
        """
		Clear #s of a trap in grid
		"""
        bound_len = configuration['attack_size_length']
        for i in xrange(pos[0] - bound_len, pos[0] + bound_len):
            for j in xrange(pos[2] - bound_len, pos[2] + bound_len):
                self.scene_grid[i][j].value = '.'

    def setup_trap_in_grid(self, pos, configuration):
        """
		Use # to indicate trap in grid
		"""
        bound_len = configuration['attack_size_length']
        for i in xrange(pos[0] - bound_len, pos[0] + bound_len):
            for j in xrange(pos[2] - bound_len, pos[2] + bound_len):
                self.scene_grid[i][j].value = '#'

    def handle_player_setup_trap(self, msg, client_hid):
        from common.events import MsgBuyResult
        from Trap import Trap
        print "in setup trap"
        if client_hid not in self.player_map:
            return
        player = self.player_map[client_hid]
        if msg.ttype < 0 or msg.ttype >= len(self.trap_conf['trap_prefabs']):
            print "Setup trap error: ", msg.ttype
            return
        configuration = self.trap_conf['trap_prefabs'][msg.ttype]
        pos = [msg.px, msg.py, msg.pz]
        # check position legal, no collision
        if not self.check_trap_setup_position_legal(pos, configuration):
            print "trap position illegal: ", pos
            return
        # can afford ?
        if player.buy(configuration['cost']):
            print "Buy and setup a trap"
            tid = self.generate_trap_id()
            trap = Trap(tid, msg.ttype, pos, player, configuration, player.get_trap_level_multiply())
            self.traps[tid] = trap
            # Mark in grid
            self.setup_trap_in_grid(pos, configuration)
            # send buy result, just update player's money
            msgBuyResult = MsgBuyResult(player.client_hid, 0, player.skill_level, player.gold_num)
            self.host.sendClient(player.client_hid, msgBuyResult.marshal())
            # send to other client
            self.broadcast(trap.generate_born_msg(), not_send=player)
        else:
            print "Not enough gold"

    def update_arrows_behavior(self):
        """
		Update arrow position, detect collision
		"""
        dead_arrows = []

        for arrow in self.arrows.itervalues():
            if arrow.is_dead():
                dead_arrows.append(arrow.aid)
                continue
            arrow.move()
            if arrow.check_hit_enemy(self.enemies, self):
                dead_arrows.append(arrow.aid)  # send enemy get hurt message
                continue
            if arrow.check_hit_player(self.player_map, self):
                print "hit player"
                dead_arrows.append(arrow.aid)  # send player get hurt message
                continue
            if arrow.check_hit_wall_floor(self.scene_grid):
                dead_arrows.append(arrow.aid)
        # delete dead arrows
        for aid in dead_arrows:
            del self.arrows[aid]

    def generate_arrow_id(self):
        aid = self.arrow_count
        self.arrow_count += 1
        self.arrow_count = divmod(self.arrow_count, self.arrow_conf['max_arrow_id_num'])[1]
        return aid

    def spawn_an_arrow(self, msg, atype, player):
        """
		Spawn an arrow, send message to all players
		"""
        from Arrow import Arrow
        from common.events import MsgArrowBorn
        aid = self.generate_arrow_id()
        arrow = Arrow(aid, atype, [msg.px, msg.py, msg.pz], [msg.dx, msg.dy, msg.dz],
                      player, self.arrow_conf['arrow_prefab'][atype], player.get_skill_level_multiply())
        self.arrows[aid] = arrow
        # broadcast message
        msg = MsgArrowBorn(aid, atype, msg.px, msg.py, msg.pz, msg.dx, msg.dy, msg.dz)
        self.broadcast(msg, not_send=player)

    def handle_player_normal_attack(self, msg, client_hid):
        """
		Player normal attack, generate an arrow
		"""
        if client_hid not in self.player_map:
            return
        player = self.player_map[client_hid]
        if player.try_attack(0, msg):
            self.spawn_an_arrow(msg, 0, player)

    def handle_player_skill_attack(self, msg, client_hid):
        """
		Player skill attack, generate five arrows
		"""
        if client_hid not in self.player_map:
            return
        player = self.player_map[client_hid]
        if player.try_attack(1, msg):
            self.spawn_an_arrow(msg, 1, player)

    def handle_player_move(self, msg, client_hid):
        """
		Handle player move, need to check legal
		"""
        if client_hid not in self.player_map:
            return
        player = self.player_map[client_hid]
        if player.is_dead():
            return
        new_pos = [msg.px, msg.py, msg.pz]
        if player.is_player_move_legal(new_pos, self.scene_grid):
            player.update_position(new_pos)
        else:
            pass
        # should log here
        # print "Error: player move illegal"
        # broadcast move info to other player
        self.broadcast(msg, not_send=player)

    def update_enemy_behavior(self):
        """
		Update enemy position, escape, try attack player
		"""
        escape_eids = []
        dead_eids = []
        for enemy in self.enemies.itervalues():
            if type(enemy) is not Enemy:
                continue
            if enemy.is_dead():
                dead_eids.append(enemy.eid)
                continue
            enemy.update_position(self.player_map.itervalues(), self.scene_grid)
            move_msg = enemy.generate_move_msg()
            if move_msg:
                self.broadcast(move_msg)
            # check escape
            if enemy.check_escape(self.enemy_escape_range):
                escape_eids.append(enemy.eid)

        # delete dead enemies
        for eid in dead_eids:
            self.group_enemy_dead_escape_num += 1
            del self.enemies[eid]

        # handle enemy escape
        for eid in escape_eids:
            self.group_enemy_dead_escape_num += 1
            self.handle_enemy_escape(self.enemies[eid])

        # enemy try attack
        for enemy in self.enemies.itervalues():
            enemy.attack(self)

        if self.group_enemy_dead_escape_num == self.enemy_groups[self.spawn_group_id]:
            self.spawn_group_id += 1
            if self.spawn_group_id >= len(self.enemy_groups):
                self.win_game()
            else:
                self.already_spawn_count = 0
                self.group_enemy_dead_escape_num = 0
                self.last_group_end_time = time.time()

    def handle_enemy_escape(self, enemy):
        """
		An enemy escape
		"""
        self.broadcast(enemy.generate_escape_msg())
        # self.enemies[enemy.eid] = time.time()
        del self.enemies[enemy.eid]
        self.escape_enemies_num += 1
        # game over
        if self.escape_enemies_num >= self.max_escape_enemies_num:
            self.lose_game()

    def generate_enemy_id(self):
        # eid = -1
        # for i in xrange(len(self.enemies)):
        # 	if type(self.enemies[i]) is not Enemy and time.time() - self.enemies[i] >= self.enemy_id_reuse_time:
        # 		eid = i
        # 		break
        # if eid == -1:
        # 	eid = len(self.enemies)
        # 	self.enemies.append(None)
        eid = self.enemy_count
        self.enemy_count += 1
        return eid

    def spawn_one_enemy(self):
        """
		Spawn one enemy with random type and random position
		"""
        import random
        from common import Util

        if self.last_group_end_time is not None and \
                                time.time() - self.last_group_end_time < self.scene_conf['time_between_enemy_group']:
            return

        if self.already_spawn_count >= self.scene_conf['enemy_group_num'][self.spawn_group_id]:
            return

        self.already_spawn_count += 1

        # random prefab
        enemy_prefabs = self.enemy_conf['enemy_prefab']
        enemy_prefab_idx = Util.get_random_index_with_distribution(self.scene_conf['enemy_spawn_distribution'])

        # random spawn transform
        spawn_transforms = self.scene_conf['enemy_spawn_transforms']
        spawn_transform_idx = random.randint(0, len(spawn_transforms) - 1)
        spawn_transform = deepcopy(spawn_transforms[spawn_transform_idx])

        # create enemy
        ep = enemy_prefabs[enemy_prefab_idx]
        eid = self.generate_enemy_id()
        enemy = Enemy(eid, spawn_transform[0:3], spawn_transform[3:6], deepcopy(self.scene_conf['target_position']), ep)
        self.enemies[eid] = enemy
        # send spawn message
        spawn_msg = enemy.generate_spawn_msg()
        self.broadcast(spawn_msg)

    def load_scene_map_grid(self, map_filename):
        """
		Load scene map grid
		"""
        from common.PathFinding import Node
        try:
            with open(map_filename) as f:
                i = 0
                j = 0
                for line in f:
                    nodes = []
                    for c in line.strip():
                        nodes.append(Node(c, [i, j]))
                        j += 1
                    i += 1
                    j = 0
                    self.scene_grid.append(nodes)
        except:
            raise
