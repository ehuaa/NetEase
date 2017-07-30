import sys
import time

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')

from managerbase import ManagerBase
from MsgCommon import MsgSCGameOver,MsgSSGameOver,MsgSCGameWin
import conf
from math3d import MathAuxiliary

class CombatManager(ManagerBase):
    def __init__(self, sv):
        super(CombatManager, self).__init__()
        self.sv = sv
        self.enemyWinNum = 1
        self.currentenemyArrivalNum = 0
        self.stageNum = 0
        self.enemyAttackProcessTime = time.time()

    def _initMsgHandlers(self):
        self._registerMsgHandler(conf.MSG_CS_GAME_REPLAY, self.GameReplay)

    def GameReplay(self, host, cid ,msg):
        self.currentenemyArrivalNum = 0
        self.stageNum = 0

    def IncrementStageNum(self):
        self.stageNum = self.stageNum + 1
        if self.stageNum > 2:
            msg = MsgSCGameWin()
            self._msgToAllClient(msg)
            return False
        return True

    def PlayerFireLight(self,msg):
        try:
            val = MathAuxiliary.LineHitSphere(self.sv.gamescene.GetEntityData(msg.entityID1).position, [0,0,1], self.sv.gamescene.GetEntityData(msg.entityID2).position, 3)
        except:
            return

        if val == False:
            return

        data = self.sv.gamescene.GetEnemyData(msg.entityID2)

        if data == None:
            return

        blood = data.blood
        blood = blood - 10

        if blood <= 0:
            blood = 0
            data.blood = blood
            self.sv.enemyManager.DestroyEnemy(msg.entityID2)
            self.sv.economySys.AddMoney(self.sv.gamescene.GetEntityData(msg.entityID1).userID, 10)
        else:
            data.blood = blood

    def EnemyArrival(self):
        self.currentenemyArrivalNum = self.currentenemyArrivalNum + 1
        if self.currentenemyArrivalNum >= self.enemyWinNum:
            msg = MsgSSGameOver()
            self.sv.SendMessageSS(msg)
            msg = MsgSCGameOver()
            for cid, uid in self.liveclients.items():
                self.sv.host.sendClient(cid, msg.getPackedData())

    def PlayerFireArea(self,msg):
        try:
            val = MathAuxiliary.LineHitSphere(self.sv.gamescene.GetEntityData(msg.entityID1).position, [0, 0, 1],self.sv.gamescene.GetEntityData(msg.entityID2).position, 3)
        except:
            return

        if val == False:
            return

        retData = self.sv.enemyManager.FindEnemiesInCircle(self.sv.gamescene.GetEntityData(msg.entityID2).position, 10)

        for val in retData:
            blood = val.blood
            blood = blood - 100

            if blood <= 0:
                blood = 0
                val.blood = blood
                self.sv.enemyManager.DestroyEnemy(msg.entityID2)
                self.sv.economySys.AddMoney(self.sv.gamescene.GetEntityData(msg.entityID1).userID, 10)
            else:
                val.blood = blood

    def EnemyAttack(self, entityEnemy, entityPlayer):
        enemydata = self.sv.gamescene.GetEnemyData(entityEnemy)
        playerdata = self.sv.gamescene.GetEntityData(entityPlayer)
        actorattr = self.sv.gamescene.actor_attr.GetActorAttributes(playerdata.userID)

        if enemydata == None or playerdata == None or actorattr == None:
            return

        posEnemy = enemydata.position
        posPlayer =playerdata.position

        if enemydata.enemyID == 1:
            if MathAuxiliary.Distance(posEnemy, posPlayer)<4:
                newBlood = actorattr.blood - 10
                self.sv.playerManager.BloodChange(playerdata.userID, newBlood)
        else:
            if MathAuxiliary.Distance(posEnemy, posPlayer) < 20:
                newBlood = actorattr.blood - 5
                self.sv.playerManager.BloodChange(playerdata.userID, newBlood)

    def TrapAttack(self, cid, msg):
        try:
            tpos = self.sv.gamescene.GetTrapData(msg.entityID1).position
            tid = self.sv.gamescene.GetTrapData(msg.entityID1).trapID
            edata = self.sv.gamescene.GetEnemyData(msg.entityID2)
        except:
            return

        if tid == 1:
            edata.blood -= 100
            if edata.blood <= 0:
                blood = 0
                edata.blood = blood
                self.sv.enemyManager.DestroyEnemy(msg.entityID2)
        else:
            edata.speed = 1
            edata.timeStamp = time.time()

        return True

    def Process(self, host):
        pass

    def RegisterLiveClient(self, cid, uid):
        self.liveclients[cid] = uid

    def UnregisterClient(self, cid):
        if self.liveclients.has_key(cid) == False:
            return
        self.liveclients.pop(cid)