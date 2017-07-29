import sys

sys.path.append('./common')

from MsgCommon import MsgSCMoney
from managerbase import ManagerBase

class EconomySys(ManagerBase):
    def __init__(self,sv):
        super(EconomySys, self).__init__()
        self.sv = sv

    def AddMoney(self,UserID,Increment):
        acinfo = self.sv.gamescene.actor_attr.actorAttr[UserID]
        acinfo.money = acinfo.money + Increment
        self.SendMoneyChangeMessage(UserID, acinfo.money)

    def SendMoneyChangeMessage(self, UserID, NewMoneyValue):
        for cid, uid in self.liveclients.items():
            if uid == UserID:
                msg = MsgSCMoney(UserID, NewMoneyValue)
                self.sv.host.sendClient(cid, msg.getPackedData())

    def RegisterLiveClient(self, cid, uid):
        self.liveclients[cid] = uid
        #Send Initial Message
        acinfo = self.sv.gamescene.actor_attr.actorAttr[uid]
        self.SendMoneyChangeMessage(uid, acinfo.money)

    def UnregisterClient(self, cid):
        if self.liveclients.has_key(cid) == False:
            return
        self.liveclients.pop(cid)

    def SendInitPlayerMoney(self, UserID):
        acinfo = self.sv.gamescene.actor_attr.actorAttr[UserID]
        self.SendMoneyChangeMessage(UserID, acinfo.money)