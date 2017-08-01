from common.events import MsgPlayerBorn
import importlib
import time
import sqlite3


class Player(object):
    def __init__(self, client_hid, name, skill_level, trap_level, position, rotation, configuration):
        super(Player, self).__init__()
        self.client_hid = client_hid
        self.name = name
        self.is_leave_scene = False
        # basic properties
        self.health = 100
        self.gold_num = 0
        # stored properties
        self.skill_level = skill_level
        self.trap_level = trap_level
        # scene info
        self.position = position
        self.rotation = rotation

        # configuration
        self.configuration = configuration

        self.skill_level_buy_cost = self.configuration['skill_level_buy_cost']
        self.trap_level_buy_cost = self.configuration['trap_level_buy_cost']
        self.skill_level_multiply = self.configuration['skill_level_multiply']
        self.trap_level_multiply = self.configuration['trap_level_multiply']

        self.last_move_time = time.time()
        self.last_normal_attack_time = None
        self.last_skill_attack_time = None

    def generate_born_msg(self, send_to_others):
        return MsgPlayerBorn(self.client_hid, send_to_others, self.name, self.health, self.skill_level,
                             self.trap_level, self.position[0], self.position[1], self.position[2],
                             self.rotation[0], self.rotation[1], self.rotation[2])

    def get_skill_level_multiply(self):
        return self.skill_level_multiply[self.skill_level]

    def get_trap_level_multiply(self):
        return self.trap_level_multiply[self.trap_level]

    def hit_me(self, pos):
        """
		Check arrow hit body, assume arrow always before player, FIX ME !!!
		"""
        from common import Util
        if pos[1] > self.configuration['height'] or pos[1] < 0:
            # print "too high: ", self.position, self.configuration['height']
            return False
        dis = Util.vector2_distance([pos[0], pos[2]], [self.position[0], self.position[2]])
        if dis <= self.configuration['body_radius'] / 2:  # Enemy too powerful, FIX ME !!!
            return True
        # print "dis: ", dis, self.configuration['body_radius']
        return False

    def buy_trap_level(self):
        """
		Try buy trap level
		"""
        cost = self.trap_level_buy_cost[self.skill_level]
        if self.buy(cost):
            self.trap_level += 1
            if self.trap_level >= len(self.trap_level_buy_cost):
                self.trap_level = len(self.trap_level_buy_cost) - 1

    def buy_level(self, level_type):
        """
		Buy level
		"""
        from common.events import MsgBuyResult
        if level_type == 0:  # Try buy skill level
            if self.skill_level >= len(self.skill_level_buy_cost):
                print "Buy fail: max level"
                return
            cost = self.skill_level_buy_cost[self.skill_level]
            if self.buy(cost):
                self.skill_level += 1
                return MsgBuyResult(self.client_hid, level_type, self.skill_level, self.gold_num)

        else:  # Try buy trap level
            if self.trap_level >= len(self.trap_level_buy_cost):
                print "Buy fail: max level"
                return
            cost = self.trap_level_buy_cost[self.trap_level]
            if self.buy(cost):
                self.trap_level += 1
                return MsgBuyResult(self.client_hid, level_type, self.trap_level, self.gold_num)
        return None

    def set_leave_scene(self):
        self.is_leave_scene = True

    def is_dead(self):
        """
		Consider player dead if he leave scene
		"""
        if self.is_leave_scene:
            return True
        return self.health <= 0

    def get_reward(self, gold_num):
        if self.is_dead():
            return
        self.gold_num += gold_num
        if self.gold_num >= self.configuration['max_gold_num']:
            self.gold_num = self.configuration['max_gold_num']

    def buy(self, cost):
        """
		Try to buy something
		"""
        if self.is_dead():
            return
        if cost < 0:
            print "Error buy trap, negative cost"
            return False
        if cost <= self.gold_num:
            self.gold_num -= cost
            return True
        return False

    def check_attack_position_direction(self, msg):
        """
		Check attack position and direction
		"""
        # FIX ME !!!
        return True

    def try_attack(self, attack_mode, msg):
        if self.is_dead():
            return False
        if not self.check_attack_position_direction(msg):
            return False
        now = time.time()
        if attack_mode == 0:  # normal attack
            if self.last_normal_attack_time is not None and \
                                    now - self.last_normal_attack_time < self.configuration[
                        'normal_shoot_time_interval']:
                return False
            self.last_normal_attack_time = now
            return True
        else:  # skill attack
            if self.last_skill_attack_time is not None and \
                                    now - self.last_skill_attack_time < self.configuration['skill_shoot_time_interval']:
                return False
            self.last_skill_attack_time = now
            return True

    def get_hurt(self, damage, scene):
        """
		Player get hurt, may be dead
		"""
        if self.is_dead():
            return
        from common.events import MsgPlayerGetHurt
        self.health -= damage
        if self.health <= 0:  # dead
            self.health = 0

        # send message to everyone
        msg = MsgPlayerGetHurt(self.client_hid, self.health)
        scene.broadcast(msg)

    def update_position(self, pos):
        if self.is_dead():
            return
        self.position[0] = pos[0]
        self.position[1] = pos[1]
        self.position[2] = pos[2]
        self.last_move_time = time.time()

    def is_player_move_legal(self, new_pos, scene_grid):
        """
		Player move test
		"""
        from common.PathFinding import PathFinding
        if self.is_dead():  # already dead
            return False
        # check whether there is a path
        path = PathFinding.run(self.position, new_pos, scene_grid)
        if path is None:
            return False
        # check move distance
        if not self.check_move_distance_legal(new_pos):
            return False
        return True

    def check_move_distance_legal(self, new_pos):
        """
		Max distance estimation, not accurate enough
		"""
        if self.is_dead():
            return False
        from common import Util
        now = time.time()
        max_dis = (now - self.last_move_time) * self.configuration['move_speed'] + self.configuration[
            'move_delay_error']
        dis = Util.vector3_distance(self.position, new_pos)
        if dis > max_dis:
            return False
        return True
