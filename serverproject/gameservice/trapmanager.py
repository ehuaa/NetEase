import sys

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')

class TrapManager(object):
    def __init__(self, gameScene):
        super(TrapManager, self).__init__()
        self.gamescene = gameScene
        self.liveclients = {}


    def MsgHandler(self, host, msg, cid, uid):
        pass

    # Update the enemies' state
    def Process(self, host):
        if len(self.liveclients) == 0:
            return

    def RegisterLiveClient(self, host, cid, uid):
        self.liveclients[cid] = uid
        self.gamescene.sendAllTraps(host, cid, uid)

    def UnregisterClient(self, cid):
        self.liveclients.pop(cid)