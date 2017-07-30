import sys

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')
from managerbase import ManagerBase
from MsgCommon import MsgSCLoadscene,MsgSCBackpack,MsgSCTrapDie
import conf

class TrapManager(ManagerBase):
    def __init__(self, sv):
        super(TrapManager, self).__init__()
        self.sv = sv
        self.liveclients = {}

    def _initMsgHandlers(self):
        self._registerMsgHandler(conf.MSG_CS_GAME_REPLAY, self.ReplayGame)
        self._registerMsgHandler(conf.MSG_CS_TRAP_IN, self.TrapIn)
        self._registerMsgHandler(conf.MSG_CS_TRAP_ATTACK, self._trapAttack)

    def _trapAttack(self, host, cid, msg):
        if self.sv.combatManager.TrapAttack(cid, msg) == True:
            self.sv.gamescene.DestroyTrap(msg.entityID1)
            msg = MsgSCTrapDie(msg.entityID1)
            for cid,uid in self.liveclients.items():
                self.sv.host.sendClient(cid, msg.getPackedData())


    def TrapIn(self, host, cid, msg):
        backpack = self.sv.gamescene.actor_attr.GetActorAttributes(msg.userID).backpack

        if backpack.traps[msg.trapID] <= 0:
            return
        else:
            if self.sv.gamescene.mapData.GetMaskData(msg.position) == 1:
                return
            else:
                backpack.traps[msg.trapID] -= 1
                pos = msg.position
                pos[1] = 0.57
                data = self.sv.gamescene.CreateTrap(msg.trapID, pos)
                self._sendTrapToAllClients(data)
                self.SendTrapAttr(cid, msg.userID)


    def ReplayGame(self, host, cid, msg):
        if self.sv.enemyManager.gameover == False:
            self.sv.gamescene.sendALLEnemies(host, cid)
            self.SendTrapAttr(cid, msg.userID)
            return

        self.sv.gamescene.DestroyAllTrap()
        self.SendTrapAttr(cid, msg.userID)


    def Process(self, host):
        pass

    def RegisterLiveClient(self, host, cid, uid):
        self.liveclients[cid] = uid
        self._sendAllTraps(cid)
        self.SendTrapAttr(cid, uid)

    def UnregisterClient(self, cid):
        if self.liveclients.has_key(cid) == False:
            return
        self.liveclients.pop(cid)

    def _sendAllTraps(self, cid):
        for k, val in self.sv.gamescene.trapData.items():
            trapID = val.trapID
            entityID = val.entityID
            pos = val.position
            q = val.quat

            msg = MsgSCLoadscene(MsgSCLoadscene.MSG_KIND_TRAP, trapID, pos, q, entityID)
            data = msg.getPackedData()

            self.sv.host.sendClient(cid, data)

    def SendTrapAttr(self, cid, userID):
        data = self.sv.gamescene.actor_attr.GetActorAttributes(userID)
        msg = MsgSCBackpack(1, data.backpack.traps[1], 2, data.backpack.traps[2])

        self.sv.host.sendClient(cid, msg.getPackedData())

    def _sendTrapToClient(self,cid, data):
        msg = MsgSCLoadscene(MsgSCLoadscene.MSG_KIND_TRAP, data.trapID, data.position, data.quat, data.entityID)
        data = msg.getPackedData()
        self.sv.host.sendClient(cid, data)

    def _sendTrapToAllClients(self, data):
        for cid,uid in self.liveclients.items():
            self._sendTrapToClient(cid, data)