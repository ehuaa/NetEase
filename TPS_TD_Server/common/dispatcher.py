# -*- coding: GBK -*-


class Service(object):
	def __init__(self, sid=0):
		super(Service, self).__init__()

		self.service_id = sid
		self.__command_map = {}

	def handle(self, msg, client_hid):
		cid = msg.cid
		if not cid in self.__command_map:
			raise Exception('bad command %s' % cid)

		f = self.__command_map[cid]
		return f(msg, client_hid)
	
	def register_command(self, cid, f):
		self.__command_map[cid] = f
	
	def register_commands(self, command_dict):
		self.__command_map = {}
		for cid in command_dict:
			self.register_command(cid, command_dict[cid])


class Dispatcher(object):
	def __init__(self):
		super(Dispatcher, self).__init__()
		self.__service_map = {}

	def dispatch(self, msg, client_hid):
		sid = msg.sid
		if sid not in self.__service_map:
			return False
		svc = self.__service_map[sid]
		svc.handle(msg, client_hid)
		return True
	
	def register(self, sid, svc):
		self.__service_map[sid] = svc
