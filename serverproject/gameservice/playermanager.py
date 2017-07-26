import sys

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')
from MsgCommon import MsgSCMoveTo

class PlayerManager(object):
    def __init__(self, gameScene):
        super(PlayerManager, self).__init__()
        self.gamescene = gameScene
        self.liveclients = {}


    def MsgHandler(self, host, cid, msg):
        self.PlayerMove(host, cid, msg)

    def PlayerMove(self, host, cid, msg):
        userData = self.gamescene.playerData[repr(msg.GetUserID())]

        if self.gamescene.routerManager.MovePermission(userData['EntityID'], msg.GetMovement()) == True:
            self.PlayerMovementNotify(host, cid, msg.GetUserID(),int(userData['EntityID']), msg.GetMovement())

    def PlayerMovementNotify(self,host, cid, userID,entityID, movement):
        msg = MsgSCMoveTo(entityID, userID, movement)
        data =msg.getPackedData()
        for v,k in self.liveclients.items():
            host.sendClient(v, data)

    def Process(self, host):
        if len(self.liveclients) == 0:
            return

    def RegisterLiveClient(self, host, cid, uid):
        self.liveclients[cid] = uid
        self.gamescene.sendAllPlayers(host, cid, uid)

    def UnregisterClient(self, cid):
        self.liveclients.pop(cid)