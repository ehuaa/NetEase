# -*- coding: GBK -*-


class Service(object):
    def __init__(self, sid=0):
        super(Service, self).__init__()

        self.service_id = sid
        self.__command_map = {}

    def handle(self, msg, client_hid):
        cmdid = msg.cmdid
        if not cmdid in self.__command_map:
            raise Exception('bad command %s' % cmdid)

        f = self.__command_map[cmdid]
        return f(msg, client_hid)

    def register_command(self, cmdid, f):
        self.__command_map[cmdid] = f

    def register_commands(self, command_dict):
        self.__command_map = {}
        for cmdid in command_dict:
            self.register_command(cmdid, command_dict[cmdid])


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
