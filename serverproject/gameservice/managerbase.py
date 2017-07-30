class ManagerBase(object):
    def __init__(self):
        self.liveclients={}
        self.msgHandlers={}
        self.sv = None
        self._initMsgHandlers()

    def Process(self, host):
        pass

    def _initMsgHandlers(self):
        pass

    def MsgHandler(self, host, cid, msg):
        for handler in self.msgHandlers[msg.command]:
            handler(host, cid, msg)

    def _registerMsgHandler(self, msg, func):
        if self.msgHandlers.has_key(msg) == False:
            self.msgHandlers[msg] = []

        if func not in self.msgHandlers[msg]:
            self.msgHandlers[msg].append(func)

    def _unregisterMsgHandler(self, msg, func):
        if self.msgHandlers.has_key(msg) == False:
            return

        if func in self.msgHandlers[msg]:
            self.msgHandlers[msg].remove(func)

    def RegisterLiveClient(self, cid, uid):
        self.liveclients[cid] = uid

    def UnregisterClient(self, cid):
        if self.liveclients.has_key(cid) == False:
            return
        self.liveclients.pop(cid)

    def _initMsgHandlers(self):
        pass

    def _msgToAllClient(self, msg):
        data = msg.getPackedData()
        for cid, uid in self.liveclients.items():
            self.sv.host.sendClient(cid, data)