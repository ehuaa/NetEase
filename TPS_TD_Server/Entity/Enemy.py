from common import Util
from common.PathFinding import PathFinding
import time


class Enemy(object):
	def __init__(self, eid, position, spawn_rotation, target_position, configuration):
		super(Enemy, self).__init__()
		self.eid = eid
		# Properties
		self.health = configuration['health']
		self.configuration = configuration
		# scene info
		self.position = position
		self.spawn_rotation = spawn_rotation
		self.is_position_update = False
		self.target_position = target_position
		# attack
		self.attack_player = None
		self.attack_position = None
		self.last_attack_time = None
		# path
		self.path = None
		# get hurt
		self.stun_time = None
		self.stun_start_time = None
		# slow down
		self.slow_start_time = None
		self.slow_time = None
		self.slow_percentage = None
		self.slow_counter = 0.0

	def is_dead(self):
		return self.health <= 0

	def get_body_radius(self):
		return self.configuration['body_radius']

	def in_attack_range(self, pos, attack_radius):
		dis = Util.vector2_distance([pos[0], pos[2]], [self.position[0], self.position[2]])
		if dis <= self.configuration['body_radius'] + attack_radius:
			return True
		return False

	def hit_me(self, pos):
		"""
		Check arrow hit body, assume arrow always before enemy, FIX ME !!!
		"""
		if pos[1] > self.configuration['height'] or pos[1] < 0:
			# print "too high: ", self.position, self.configuration['height']
			return False
		dis = Util.vector2_distance([pos[0], pos[2]], [self.position[0], self.position[2]])
		if dis <= self.configuration['body_radius']:
			return True
		# print "dis: ", dis, self.configuration['body_radius']
		return False

	def get_hurt(self, player, damage, damage_multiply, scene):
		"""
		Get hurt, may be stunning
		"""
		from common.events import MsgEnemyGetHurt
		self.health -= int(damage['health_dec'] * damage_multiply)
		if self.health <= 0:
			self.health = 0
			player.get_reward(self.configuration['kill_reward'])
		# stunning
		if 'stun' in damage:
			self.stun_time = damage['stun']
			if self.stun_time > 0:
				self.stun_start_time = time.time()
			msg = MsgEnemyGetHurt(self.eid, self.health, 1, 0, player.client_hid, player.gold_num)
		# speed slow
		elif 'speed_slow' in damage:
			self.slow_percentage = damage['speed_slow']
			self.slow_time = damage['speed_slow_time']
			self.slow_counter = 0
			self.slow_start_time = time.time()
			msg = MsgEnemyGetHurt(self.eid, self.health, 0, 1, player.client_hid, player.gold_num)
		else:
			msg = MsgEnemyGetHurt(self.eid, self.health, 0, 0, player.client_hid, player.gold_num)
		# broadcast message
		scene.broadcast(msg)

	def is_stunning(self):

		if self.stun_start_time is None:
			return False

		if time.time() - self.stun_start_time > self.stun_time:
			self.stun_start_time = None
			return False

		# recover
		return True

	def attack(self, scene):
		"""
		Enemy attack player
		"""
		from Entity.Arrow import Arrow
		from common.events import MsgArrowBorn

		if self.is_dead():
			return

		if self.is_stunning():
			return

		if self.attack_player is None:
			# attack no one
			return

		if self.attack_player.is_dead():
			return

		if Util.vector3_distance(self.position, self.attack_position) > self.configuration['attack_stop_distance']:
			# not close enough
			return
		now = time.time()
		if self.last_attack_time and now - self.last_attack_time < self.configuration['time_between_attack']:
			return
		self.last_attack_time = now
		# Attack
		if self.configuration['attack_mode'] == 0:  # near attack
			self.attack_player.get_hurt(self.configuration['damage'], scene)
		else:  # remote attack
			# generate an arrow of atype -1
			aid = scene.generate_arrow_id()
			pos = self.position
			apos = self.attack_player.position
			direct = Util.vector3_normalize([apos[0] - pos[0], 0, apos[2] - pos[2]])
			# born in front of body
			born_pos = Util.vector3_add(Util.vector3_inner_product(direct, self.configuration['body_radius']), pos)
			arrow = Arrow(aid, -1, [born_pos[0], self.configuration['height'] / 2, born_pos[2]],
						  direct, None, scene.arrow_conf['enemy_arrow_prefab'])
			scene.arrows[aid] = arrow
			# broadcast message
			msg = MsgArrowBorn(aid, -1, born_pos[0], self.configuration['height'] / 2,
							   born_pos[2], direct[0], direct[1], direct[2])
			scene.broadcast(msg)

	def generate_spawn_msg(self):
		"""
		Generate enemy spawn message
		"""
		from common.events import MsgEnemyBorn
		return MsgEnemyBorn(self.eid, self.configuration['etype'], self.health, self.configuration['damage'],
							self.configuration['kill_reward'], self.position[0], self.position[1],
							self.position[2], self.spawn_rotation[0], self.spawn_rotation[1], self.spawn_rotation[2])

	def generate_move_msg(self):
		"""
		Generate enemy move message if enemy position has been updated
		"""
		from common.events import MsgEnemyMove
		if self.is_position_update:
			self.is_position_update = False
			return MsgEnemyMove(self.eid, self.position[0], self.position[1], self.position[2])
		return None

	def generate_escape_msg(self):
		"""
		Generate enemy escape message
		"""
		from common.events import MsgEnemyEscape
		return MsgEnemyEscape(self.eid)

	def check_escape(self, escape_range):
		"""
		Is enemy run away successfully
		"""
		if self.is_dead():
			return False
		# check escape
		if Util.vector3_distance(self.position, self.target_position) <= escape_range:
			return True
		return False

	def check_slow(self):
		"""
		Enemy slow down, not move
		"""
		if self.slow_start_time is None:
			return False
		now = time.time()
		if now - self.slow_start_time >= self.slow_time:
			# slow over
			self.slow_start_time = None
			self.slow_percentage = 1.0
			self.slow_counter = 0.0
			return False
		self.slow_counter += self.slow_percentage
		if self.slow_counter >= 1.0:
			# can move
			self.slow_counter -= 1.0
			return False
		return True

	def update_position(self, players, scene_grid):
		"""
		Update enemy position base on players and scene_grid
		"""
		if self.is_dead():
			return

		if self.is_stunning():
			return

		if self.check_slow():
			return

		close_player = None
		min_dis = None
		for player in players:
			if player is None:
				continue
			if player.is_dead():
				continue
			dis = Util.vector3_distance(player.position, self.position)
			# print player.position
			if dis < self.configuration['visible_range']:
				if not close_player or dis < min_dis:
					min_dis = dis
					close_player = player
		if close_player:  # find player
			self.attack_player = close_player
			# Assume visible range > attack_stop_distance
			if min_dis < self.configuration['attack_stop_distance']:  # no need to move
				self.is_position_update = False
				self.attack_position = [x for x in player.position]
				return
			else:  # need to move
				self.find_next_position(close_player, scene_grid)
		else:  # go to target position
			if self.attack_position or self.path is None:  # enemy attack player recently, need to find a new path
				self.attack_position = None
				self.attack_player = None
				new_path = PathFinding.run(self.position, self.target_position, scene_grid)
				if new_path:  # assign when we find a path
					self.path = new_path
				else:
					# should log here
					print "Find path error"
			# update position
			self.update_position_from_path()

	def update_position_from_path(self):
		if self.path is None or len(self.path) < 1:
			print "None path error"
			return
		self.position[0], self.position[2] = self.path[0].point[0], self.path[0].point[1]  # no y axis
		self.path = self.path[1:]
		self.is_position_update = True

	def find_next_position(self, player, scene_grid):
		"""
		Find next position, may need to find a new path.
		"""
		if not (self.attack_position and Util.vector3_equal(self.attack_position, player.position)):
			self.attack_position = [x for x in player.position]
			new_path = PathFinding.run(self.position, self.attack_position, scene_grid)
			if new_path:  # assign when we find a path
				self.path = new_path
			else:
				# should log here
				print "Find path error"
		# update position
		self.update_position_from_path()
