import time
from common import Util


class Trap(object):
	def __init__(self, tid, ttype, position, player, configuration, damage_multiply=1.0):
		super(Trap, self).__init__()
		self.tid = tid
		self.ttype = ttype
		self.position = position
		self.player = player
		self.configuration = configuration
		self.trigger_times = configuration['trigger_times']
		self.trigger_range = configuration['trigger_range']
		self.last_trigger_time = None
		# damage multiply must be set when object is born
		self.damage_multiply = damage_multiply

	def pos_in_trigger_range(self, enemy):
		"""
		Check pos trigger traps
		"""
		dis = Util.vector3_distance(self.position, enemy.position)
		return dis <= self.trigger_range + enemy.get_body_radius()

	def pos_in_attack_range(self, enemy):
		"""
		Assume attack range equal to trigger range
		"""
		dis = Util.vector3_distance(self.position, enemy.position)
		return dis <= self.trigger_range + enemy.get_body_radius()

	def try_trigger(self, enemies, scene):
		if self.is_dead():
			return
		now = time.time()
		if self.last_trigger_time is not None and \
					now - self.last_trigger_time < self.configuration['time_between_trigger']:
			return
		is_trigger = False
		for enemy in enemies.itervalues():
			if self.pos_in_trigger_range(enemy):
				is_trigger = True
				break
		if not is_trigger:
			return
		self.trigger_times -= 1
		self.last_trigger_time = time.time()
		print "Trap trigger"
		for enemy in enemies.itervalues():
			if self.pos_in_attack_range(enemy):
				enemy.get_hurt(self.player, self.configuration['damage'], self.damage_multiply, scene)
		# scene.broadcast(self.generate_trigger_msg())

	def is_dead(self):
		return self.trigger_times <= 0

	def generate_born_msg(self):
		from common.events import MsgTrapBorn
		return MsgTrapBorn(self.tid, self.ttype, self.position[0], self.position[1], self.position[2])

	# def generate_trigger_msg(self):
	# 	from common.events import MsgTrapTrigger
	# 	return MsgTrapTrigger(self.tid)
	#
	# def generate_dead_msg(self):
	# 	from common.events import MsgTrapDead
	# 	return MsgTrapDead(self.tid)

