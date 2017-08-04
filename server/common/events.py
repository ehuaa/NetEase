# -*- coding: GBK -*-
import conf
from header import SimpleHeader


class MsgSCLoginResult(SimpleHeader):
	def __init__(self, ok=0, message=''):
		super(MsgSCLoginResult, self).__init__(conf.MSG_SC_LOGIN_RESULT)
		self.append_param('ok', ok, 'i')
		self.append_param('message', message, 's')

class MsgCSRegister(SimpleHeader):
	def __init__(self, username='', password=''):
		super(MsgCSRegister, self).__init__(conf.MSG_CS_REGISTER)
		self.append_param('username', username, 's')
		self.append_param('password', password, 's')
		self.sid = conf.USER_SERVICES
		self.cmdid = 0

class MsgCSLogin(SimpleHeader):
	def __init__(self, username='', password=''):
		super(MsgCSLogin, self).__init__(conf.MSG_CS_LOGIN)
		self.append_param('username', username, 's')
		self.append_param('password', password, 's')
		self.sid = conf.USER_SERVICES
		self.cmdid = 1

class MsgCSLogout(SimpleHeader):
	def __init__(self, client_id=-1):
		super(MsgCSLogout, self).__init__(conf.MSG_CS_LOGOUT)
		self.append_param('client_id', client_id, 'i')
		self.sid = conf.USER_SERVICES
		self.cmdid = 2

class MsgSCStartGame(SimpleHeader):
	def __init__(self):
		super(MsgSCStartGame, self).__init__(conf.MSG_SC_START_GAME)

class MsgSCPlayerBorn(SimpleHeader):
	def __init__(self, pid, ptype, name, health, px, py, pz, rx, ry, rz):
		super(MsgSCPlayerBorn, self).__init__(conf.MSG_SC_PLAYER_BORN)
		self.append_param('id', pid, 'i')
		self.append_param('ptype', ptype, 'i')  # ptype: 0->myself, 1->others
		self.append_param('name', name, 's')
		self.append_param('health', health, 'i')
		self.append_param('px', px, 'f')
		self.append_param('py', py, 'f')
		self.append_param('pz', pz, 'f')
		self.append_param('rx', rx, 'f')
		self.append_param('ry', ry, 'f')
		self.append_param('rz', rz, 'f')


class MsgCSPlayerMove(SimpleHeader):
	def __init__(self, pid=-1, px=0, py=0, pz=0, rx=0.0, ry=0.0, rz=0.0):
		super(MsgCSPlayerMove, self).__init__(conf.MSG_CS_PLAYER_MOVE)
		self.append_param('id', pid, 'i')
		self.append_param('px', px, 'f')
		self.append_param('py', py, 'f')
		self.append_param('pz', pz, 'f')
		self.append_param('rx', rx, 'f')
		self.append_param('ry', ry, 'f')
		self.append_param('rz', rz, 'f')
		self.sid = conf.ARENA_SERVICES
		self.cmdid = 0

class MsgSCGameWin(SimpleHeader):
	def __init__(self):
		super(MsgSCGameWin, self).__init__(conf.MSG_SC_GAME_WIN)


class MsgSCGameOver(SimpleHeader):
	def __init__(self):
		super(MsgSCGameOver, self).__init__(conf.MSG_SC_GAME_OVER)