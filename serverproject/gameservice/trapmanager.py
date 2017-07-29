import sys

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')
from managerbase import ManagerBase

class TrapManager(ManagerBase):
    def __init__(self, sv):
        super(TrapManager, self).__init__()
        self.sv = sv
        self.liveclients = {}

    # Update the enemies' state
    def Process(self, host):
        if len(self.liveclients) == 0:
            return

    def RegisterLiveClient(self, host, cid, uid):
        self.liveclients[cid] = uid
        self.sv.gamescene.sendAllTraps(host, cid)

    def UnregisterClient(self, cid):
        if self.liveclients.has_key(cid) == False:
            return
        self.liveclients.pop(cid)