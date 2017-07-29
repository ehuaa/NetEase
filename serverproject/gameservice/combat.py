import sys

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')

from managerbase import ManagerBase
from MsgCommon import MsgSCGameOver,MsgSSGameOver,MsgSCGameWin
import conf

class CombatManager(ManagerBase):
    def __init__(self, sv):
        super(CombatManager, self).__init__()
        self.sv = sv
        self.enemyWinNum = 1
        self.currentenemyArrivalNum = 0
        self.stageNum = 0

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
            #Send Message to other service
            return False
        return True

    def PlayerFireLight(self,msg):
        # Not Implemented (Is it a legal attack?)

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
        pass

    def _EnemyFireAttack(self, EntityID):
        pass

    def _EnemyFireDistance(self, EntityID, direct):
        pass

    def EnemyAttack(self):
        pass

    def TrapAttack(self):
        pass

    def Process(self, host):
        self.EnemyAttack()
        self.TrapAttack()

    def RegisterLiveClient(self, cid, uid):
        self.liveclients[cid] = uid

    def UnregisterClient(self, cid):
        if self.liveclients.has_key(cid) == False:
            return
        self.liveclients.pop(cid)