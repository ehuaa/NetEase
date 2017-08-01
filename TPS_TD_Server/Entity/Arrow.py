import time
from common import Util


class Arrow(object):
	def __init__(self, aid, atype, position, direction, player, configuration, damage_multiply=1.0):
		super(Arrow, self).__init__()
		self.aid = aid
		self.atype = atype   # atype == 1 -> enemy shooting arrow
		self.position = position
		self.direction = direction
		self.shooter = player
		self.configuration = configuration
		self.born_time = time.time()
		self.last_move_time = time.time()
		# damage multiply must be set when the object is born, important!
		self.damage_multiply = damage_multiply
		# consider arrow size
		# self.move_forward(configuration['arrow_length'])  FIX ME !!!!!!!

	def is_dead(self):
		if time.time() - self.born_time >= self.configuration['duration']:
			return True
		return False

	def move_forward(self, s):
		self.position = Util.vector3_add(self.position, Util.vector3_inner_product(self.direction, s))

	def move(self):
		now = time.time()
		t = now - self.last_move_time
		s = self.configuration['speed'] * t
		self.move_forward(s)
		# print self.direction, s, movement, self.position
		self.last_move_time = now

	def check_hit_enemy(self, enemies, scene):
		"""
		check the arrow hit an enemy, the current arrow may be shooting by an remote attack enemy
		"""
		if self.atype == -1:  # enemy shooting arrow
			return False

		if self.atype == 0:  # normal attack
			for enemy in enemies.itervalues():
				if not enemy.hit_me(self.position):
					continue
				# handle enemy get hurt
				enemy.get_hurt(self.shooter, self.configuration['damage'], self.damage_multiply, scene)
				# send dead msg
				return True
			return False
		else:  # range attack
			is_hit = False
			for enemy in enemies.itervalues():
				if not enemy.hit_me(self.position):
					continue
				is_hit = True
				break
			if not is_hit:
				return False

			# handle enemy get damage
			for enemy in enemies.itervalues():
				if enemy.in_attack_range(self.position, self.configuration['attack_range']):
					enemy.get_hurt(self.shooter, self.configuration['damage'], self.damage_multiply, scene)
			return True

	def check_hit_player(self, players, scene):
		"""
		Check remote-attack enemy shooting player
		"""
		if self.atype != -1:  # player shooting arrow
			return False

		for player in players.itervalues():
			if not player.hit_me(self.position):
				continue
			# handle enemy get hurt
			player.get_hurt(self.configuration['damage']['health_dec'], scene)
			# send dead msg
			return True
		return False

	def check_hit_wall_floor(self, grid):
		if self.position[1] <= 0:  # floor
			return True
		x = int(self.position[0])
		y = int(self.position[2])
		if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]):
			return False
		if grid[x][y].value == '*':
			return True
		return False

	# def generate_born_msg(self):
	# 	from common.events import MsgArrowBorn
	# 	return MsgArrowBorn(self.aid, self.atype, self.position[0], self.position[1],
	# 						self.position[2], self.direction[0], self.direction[1], self.direction[2])
	#
	# def generate_move_msg(self):
	# 	from common.events import MsgArrowMove
	# 	return MsgArrowMove(self.aid,  self.position[0], self.position[1], self.position[2])
	#
	# def generate_dead_msg(self, px=None, py=None, pz=None):
	# 	from common.events import MsgArrowDead
	# 	if px is None:
	# 		return MsgArrowDead(self.aid, self.position[0], self.position[1], self.position[2])
	# 	return MsgArrowDead(self.aid, px, py, pz)
