import sys

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')
from MsgCommon import MsgSCMoveTo, MsgCSAttack, MsgSCPlayerAttack,MsgSCLoadscene, MsgSCPlayerLogout
import conf
from math3d import MathAuxiliary

class PlayerManager(object):
    def __init__(self, sv):
        super(PlayerManager, self).__init__()
        self.sv = sv
        self.liveclients = {}
        self.msgHandlers={}

        self._initMsgHandlers()

    def _initMsgHandlers(self):
        self.msgHandlers[conf.MSG_CS_ATTACK]=[]
        self.msgHandlers[conf.MSG_CS_MOVETO]=[]

        self._registerMsgHandler(conf.MSG_CS_MOVETO, self.PlayerMove)
        self._registerMsgHandler(conf.MSG_CS_ATTACK, self.PlayerAttack)


    def _registerMsgHandler(self,msg, func):
        if func not in self.msgHandlers[msg]:
            self.msgHandlers[msg].append(func)

    def _unregisterMsgHandler(self,msg, func):
        if func in self.msgHandlers[msg]:
            self.msgHandlers[msg].remove(func)

    def MsgHandler(self, host, cid, msg):
        for handler in self.msgHandlers[msg.command]:
            handler(host, cid, msg)

    def PlayerAttack(self, host, cid, msg):
        if self.sv.gamescene.GetPlayerData(msg.userID) != self.sv.gamescene.GetEntityData(msg.entityID1):
            return

        if msg.kind == MsgCSAttack.MAGIC_ATTACK and msg.entityID2 != -1:
            self.sv.combatManager.PlayerFireArea(msg)
        elif msg.kind == MsgCSAttack.WEAPON_ATTACK and msg.entityID2 != -1:
            self.sv.combatManager.PlayerFireLight(msg)

        # SendMessage to other player
        msg = MsgSCPlayerAttack(msg.userID, msg.entityID1, msg.kind)
        for c,v in self.liveclients.items():
            if c != cid:
                self.sv.host.sendClient(c, msg.getPackedData())

    def PlayerMove(self, host, cid, msg):
        userData = self.sv.gamescene.playerData[msg.GetUserID()]

        if self.sv.routerManager.MovePermission(userData.entityID, msg.GetMovement()) == True:
            userData.position = MathAuxiliary.AddVector3(userData.position, msg.GetMovement())
            self.PlayerMovementNotify(host, msg.GetUserID(),int(userData.entityID), userData.position)

    def PlayerMovementNotify(self,host, userID, entityID, newposition):
        msg = MsgSCMoveTo(entityID, userID, newposition)
        data =msg.getPackedData()
        for v,k in self.liveclients.items():
            host.sendClient(v, data)

    def Process(self, host):
        if len(self.liveclients) == 0:
            return

    def RegisterLiveClient(self, host, cid, uid):
        self.liveclients[cid] = uid
        self._newUserLogin(uid, cid)


    def UnregisterClient(self, cid):
        if self.liveclients.has_key(cid) == False:
            return
        userID = self.liveclients[cid]
        self.liveclients.pop(cid)
        self._sendUserLogout(cid, userID)

    def _sendUsersData(self, cid, val):
        userID = val.userID
        pos = val.position
        q = val.quat
        entityID = val.entityID

        msg = MsgSCLoadscene(MsgSCLoadscene.MSG_KIND_PLAYER, userID, pos, q, entityID)
        data = msg.getPackedData()

        self.sv.host.sendClient(cid, data)

    def _sendUserLogout(self,cid, uid):
        data = self.sv.gamescene.GetPlayerData(uid)
        msg = MsgSCPlayerLogout(uid, data.entityID)
        data = msg.getPackedData()

        for c,u in self.liveclients.items():
            if c != cid :
                self.sv.host.sendClient(c, data)

    def _newUserLogin(self, uid, cid):
        newUserData = self.sv.gamescene.GetPlayerData(uid)
        if newUserData == None:
            newUserData = self.sv.gamescene.CreateUserData(uid)

        for k,v in self.liveclients.items():
            self._sendUsersData(k, newUserData)
            if k != cid:
                liveUserData = self.sv.gamescene.GetPlayerData(v)
                self._sendUsersData(cid, liveUserData)
