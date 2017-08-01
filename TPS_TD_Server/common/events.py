# -*- coding: GBK -*-
import conf
from header import SimpleHeader


class MsgLoginResult(SimpleHeader):
	def __init__(self, ok=0, message=''):
		super(MsgLoginResult, self).__init__(conf.MSG_LOGIN_RESULT)
		self.append_param('ok', ok, 'i')
		self.append_param('message', message, 's')


class MsgRegister(SimpleHeader):
	def __init__(self, username='', password=''):
		super(MsgRegister, self).__init__(conf.MSG_REGISTER)
		self.append_param('username', username, 's')
		self.append_param('password', password, 's')
		self.sid = conf.USER_SERVICES
		self.cid = 0


class MsgLogin(SimpleHeader):
	def __init__(self, username='', password=''):
		super(MsgLogin, self).__init__(conf.MSG_LOGIN)
		self.append_param('username', username, 's')
		self.append_param('password', password, 's')
		self.sid = conf.USER_SERVICES
		self.cid = 1


class MsgLogout(SimpleHeader):
	def __init__(self, client_id=-1):
		super(MsgLogout, self).__init__(conf.MSG_LOGOUT)
		self.append_param('client_id', client_id, 'i')
		self.sid = conf.USER_SERVICES
		self.cid = 2


class MsgCreateRoom(SimpleHeader):
	def __init__(self):
		super(MsgCreateRoom, self).__init__(conf.MSG_CREATE_ROOM)
		self.sid = conf.USER_SERVICES
		self.cid = 3


class MsgJoinRoom(SimpleHeader):
	def __init__(self, rid=-1):
		super(MsgJoinRoom, self).__init__(conf.MSG_JOIN_ROOM)
		self.append_param('rid', rid, 'i')
		self.sid = conf.USER_SERVICES
		self.cid = 4


class MsgLeaveRoom(SimpleHeader):
	def __init__(self):
		super(MsgLeaveRoom, self).__init__(conf.MSG_LEAVE_ROOM)
		self.sid = conf.USER_SERVICES
		self.cid = 5


class MsgRoomList(SimpleHeader):
	def __init__(self, room_list_str):
		super(MsgRoomList, self).__init__(conf.MSG_ROOM_LIST)
		self.append_param('room_list_str', room_list_str, 's')


class MsgStartGame(SimpleHeader):
	def __init__(self):
		super(MsgStartGame, self).__init__(conf.MSG_START_GAME)
		self.sid = conf.USER_SERVICES
		self.cid = 6


class MsgEnemyBorn(SimpleHeader):
	def __init__(self, eid, etype, health, damage, kill_reward, px, py, pz, rx, ry, rz):
		super(MsgEnemyBorn, self).__init__(conf.MSG_ENEMY_BORN)
		self.append_param('id', eid, 'i')
		self.append_param('etype', etype, 'i')
		self.append_param('health', health, 'i')
		self.append_param('damage', damage, 'i')
		self.append_param('kill_reward', kill_reward, 'i')
		self.append_param('px', px, 'f')
		self.append_param('py', py, 'f')
		self.append_param('pz', pz, 'f')
		self.append_param('rx', rx, 'f')
		self.append_param('ry', ry, 'f')
		self.append_param('rz', rz, 'f')


class MsgEnemyMove(SimpleHeader):
	def __init__(self, eid, px, py, pz):
		super(MsgEnemyMove, self).__init__(conf.MSG_ENEMY_MOVE)
		self.append_param('id', eid, 'i')
		self.append_param('px', px, 'f')
		self.append_param('py', py, 'f')
		self.append_param('pz', pz, 'f')


class MsgEnemyAttack(SimpleHeader):
	def __init__(self, eid, px, py, pz):
		super(MsgEnemyAttack, self).__init__(conf.MSG_ENEMY_ATTACK)
		self.append_param('id', eid, 'i')
		self.append_param('px', px, 'f')
		self.append_param('py', py, 'f')
		self.append_param('pz', pz, 'f')


class MsgEnemyGetHurt(SimpleHeader):
	def __init__(self, eid, health, stun, slow, pid, gold_num):
		super(MsgEnemyGetHurt, self).__init__(conf.MSG_ENEMY_GET_HURT)
		self.append_param('id', eid, 'i')
		self.append_param('health', health, 'i')
		self.append_param('stun', stun, 'i')
		self.append_param('slow', slow, 'i')
		self.append_param('pid', pid, 'i')
		self.append_param('gold_num', gold_num, 'i')


class MsgEnemyEscape(SimpleHeader):
	def __init__(self, eid):
		super(MsgEnemyEscape, self).__init__(conf.MSG_ENEMY_ESCAPE)
		self.append_param('id', eid, 'i')


class MsgPlayerBorn(SimpleHeader):
	def __init__(self, pid, ptype, name, health, skill_level, trap_level, px, py, pz, rx, ry, rz):
		super(MsgPlayerBorn, self).__init__(conf.MSG_PLAYER_BORN)
		self.append_param('id', pid, 'i')
		self.append_param('ptype', ptype, 'i')  # ptype: 0->myself, 1->others
		self.append_param('name', name, 's')
		self.append_param('health', health, 'i')
		self.append_param('skill_level', skill_level, 'i')
		self.append_param('trap_level', trap_level, 'i')
		self.append_param('px', px, 'f')
		self.append_param('py', py, 'f')
		self.append_param('pz', pz, 'f')
		self.append_param('rx', rx, 'f')
		self.append_param('ry', ry, 'f')
		self.append_param('rz', rz, 'f')


class MsgPlayerMove(SimpleHeader):
	def __init__(self, pid=-1, px=0, py=0, pz=0, rx=0.0, ry=0.0, rz=0.0):
		super(MsgPlayerMove, self).__init__(conf.MSG_PLAYER_MOVE)
		self.append_param('id', pid, 'i')
		self.append_param('px', px, 'i')
		self.append_param('py', py, 'i')
		self.append_param('pz', pz, 'i')
		self.append_param('rx', rx, 'f')
		self.append_param('ry', ry, 'f')
		self.append_param('rz', rz, 'f')
		self.sid = conf.SCENE_SERVICES
		self.cid = 0


class MsgPlayerGetHurt(SimpleHeader):
	def __init__(self, pid, health):
		super(MsgPlayerGetHurt, self).__init__(conf.MSG_PLAYER_GET_HURT)
		self.append_param('id', pid, 'i')
		self.append_param('health', health, 'i')


class MsgPlayerNormalAttack(SimpleHeader):
	def __init__(self, pid=0, px=0, py=0, pz=0, dx=0, dy=0, dz=0):
		super(MsgPlayerNormalAttack, self).__init__(conf.MSG_PLAYER_NORMAL_ATTACK)
		self.append_param('id', pid, 'i')
		self.append_param('px', px, 'f')
		self.append_param('py', py, 'f')
		self.append_param('pz', pz, 'f')
		self.append_param('dx', dx, 'f')
		self.append_param('dy', dy, 'f')
		self.append_param('dz', dz, 'f')
		self.sid = conf.SCENE_SERVICES
		self.cid = 1


class MsgPlayerSkillAttack(SimpleHeader):
	def __init__(self, pid=0, px=0, py=0, pz=0, dx=0, dy=0, dz=0):
		super(MsgPlayerSkillAttack, self).__init__(conf.MSG_PLAYER_SKILL_ATTACK)
		self.append_param('id', pid, 'i')
		self.append_param('px', px, 'f')
		self.append_param('py', py, 'f')
		self.append_param('pz', pz, 'f')
		self.append_param('dx', dx, 'f')
		self.append_param('dy', dy, 'f')
		self.append_param('dz', dz, 'f')
		self.sid = conf.SCENE_SERVICES
		self.cid = 2


class MsgPlayerSetupTrap(SimpleHeader):
	def __init__(self, ttype=0, px=0, py=0, pz=0):
		super(MsgPlayerSetupTrap, self).__init__(conf.MSG_PLAYER_SETUP_TRAP)
		self.append_param('ttype', ttype, 'i')
		self.append_param('px', px, 'i')
		self.append_param('py', py, 'i')
		self.append_param('pz', pz, 'i')
		self.sid = conf.SCENE_SERVICES
		self.cid = 3


class MsgGameWin(SimpleHeader):
	def __init__(self):
		super(MsgGameWin, self).__init__(conf.MSG_GAME_WIN)


class MsgGameOver(SimpleHeader):
	def __init__(self):
		super(MsgGameOver, self).__init__(conf.MSG_GAME_OVER)


class MsgSceneRound(SimpleHeader):
	def __init__(self, rounds=-1, seconds=-1):
		super(MsgSceneRound, self).__init__(conf.MSG_SCENE_ROUND)
		self.append_param('rounds', rounds, 'i')
		self.append_param('seconds', seconds, 'i')


class MsgArrowBorn(SimpleHeader):
	def __init__(self, aid, atype, px, py, pz, dx, dy, dz):
		super(MsgArrowBorn, self).__init__(conf.MSG_ARROW_BORN)
		self.append_param('id', aid, 'i')
		self.append_param('atype', atype, 'i')  # atype: 0->normal, 1->skill
		self.append_param('px', px, 'f')
		self.append_param('py', py, 'f')
		self.append_param('pz', pz, 'f')
		self.append_param('dx', dx, 'f')  # send direction instead of rotation
		self.append_param('dy', dy, 'f')
		self.append_param('dz', dz, 'f')

#
# class MsgArrowMove(SimpleHeader):
# 	def __init__(self, aid, px, py, pz):
# 		super(MsgArrowMove, self).__init__(conf.MSG_ARROW_MOVE)
# 		self.append_param('aid', aid, 'i')
# 		self.append_param('px', px, 'f')
# 		self.append_param('py', py, 'f')
# 		self.append_param('pz', pz, 'f')
#
#
# class MsgArrowDead(SimpleHeader):
# 	def __init__(self, aid, px, py, pz):
# 		super(MsgArrowDead, self).__init__(conf.MSG_ARROW_DEAD)
# 		self.append_param('aid', aid, 'i')
# 		self.append_param('px', px, 'f')
# 		self.append_param('py', py, 'f')
# 		self.append_param('pz', pz, 'f')


class MsgTrapBorn(SimpleHeader):
	def __init__(self, tid, ttype, px, py, pz):
		super(MsgTrapBorn, self).__init__(conf.MSG_TRAP_BORN)
		self.append_param('id', tid, 'i')
		self.append_param('ttype', ttype, 'i')
		self.append_param('px', px, 'i')
		self.append_param('py', py, 'i')
		self.append_param('pz', pz, 'i')


# class MsgTrapTrigger(SimpleHeader):
# 	def __init__(self, tid):
# 		super(MsgTrapTrigger, self).__init__(conf.MSG_TRAP_TRIGGER)
# 		self.append_param('id', tid, 'i')
#
#
# class MsgTrapDead(SimpleHeader):
# 	def __init__(self, tid):
# 		super(MsgTrapDead, self).__init__(conf.MSG_TRAP_DEAD)
# 		self.append_param('id', tid, 'i')

class MsgBuyLevel(SimpleHeader):
	def __init__(self, level_type=0):
		super(MsgBuyLevel, self).__init__(conf.MSG_BUY_LEVEL)
		self.append_param('level_type', level_type, 'i')
		self.sid = conf.SCENE_SERVICES
		self.cid = 4


class MsgBuyResult(SimpleHeader):
	def __init__(self, pid=-1, level_type=0, level=0, gold_num=0):
		super(MsgBuyResult, self).__init__(conf.MSG_BUY_RESULT)
		self.append_param('pid', pid, 'i')
		self.append_param('level_type', level_type, 'i')
		self.append_param('level', level, 'i')
		self.append_param('gold_num', gold_num, 'i')
