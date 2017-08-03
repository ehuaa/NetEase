from managerbase import ManagerBase
from common.MsgCommon import MsgSCEnemyDie,MsgSCMoveTo,MsgSSGameOver
from common_server.timer import TimerManager

from common import conf
from common.math3d import MathAuxiliary
import random
import time

class EnemyManager(ManagerBase):
    def __init__(self, sv):
        super(EnemyManager, self).__init__()
        self.sv=sv
        self.timerDelay = None
        self.timer = None
        self.count = 0
        self.spawn = False
        self.gameover = False
        self.destination = [0,0,-70]
        self.timeStamp = time.time()
        self.enemyMoveInterval = time.time()

    def _initMsgHandlers(self):
        self._registerMsgHandler(conf.MSG_SS_GAME_OVER, self.GameOver)
        self._registerMsgHandler(conf.MSG_CS_GAME_REPLAY, self.GameReplay)
        self._registerMsgHandler(conf.MSG_CS_ENEMY_ATTACK, self.EnemyAttack)

    def GameReplay(self, host,cid ,msg):
        if self.gameover == False:
            self.sv.gamescene.sendALLEnemies(host, cid)
            return

        if self.timerDelay != None:
            self.timerDelay.cancel()

        if self.timer != None:
            self.timer.cancel()

        self.timerDelay = None
        self.timer = None
        self.count = 0
        self.spawn = False
        self.destination = [0, 0, -70]
        self.enemyMoveInterval = time.time()
        self.gameover = False

    def GameOver(self, host, cid, msg):
        self.sv.gamescene.DestroyAllEnemy()

        if self.timerDelay:
            self.timerDelay.cancel()
        if self.timer:
            self.timer.cancel()

        self.gameover = True

    def DestroyEnemy(self, entityID):
        self.sv.gamescene.DestroyEnemy(entityID)
        msg = MsgSCEnemyDie(entityID)
        for cid, uid in self.liveclients.items():
            self.sv.host.sendClient(cid, msg.getPackedData())

    def _spawEnemy(self, number, host):
        enemyID = random.randint(1, 2)
        posx = random.random() * 30
        if random.randint(1,2) == 1:
            posx = -posx

        data = self.sv.gamescene.CreateEnemy(enemyID, [posx,0,95])
        pathData = self.EnemyPathSolve(data.entityID, self.destination)
        data.pathData = pathData

        for k,v in self.liveclients.items():
            self.sv.gamescene.SendEnemy(host, k, data)

        self.count += 1
        if self.count >= number:
            self.timer.cancel()
            TimerManager.removeCancelledTasks()
            self.spawn = False

    def SpawnEnemy(self, interval, number ,host):
        self.timerDelay.cancel()
        TimerManager.removeCancelledTasks()
        self.timer = TimerManager.addRepeatTimer(interval, self._spawEnemy, number, host)

    # Update the enemies' state
    def Process(self, host):
        if len(self.liveclients) == 0 or self.gameover == True:
            return

        TimerManager.scheduler()

        #spawn enemies and broadcast to all live clients
        if len(self.sv.gamescene.enemyData) == 0 and self.spawn == False:
            if self.sv.combatManager.IncrementStageNum() == False:
                self.gameover = True
            else:
                self.timerDelay = TimerManager.addTimer(1, self.SpawnEnemy, 2, 1, host)
                self.count = 0
                self.spawn = True

        else: #Moving and attacking the Players
            self.EnemysMove()

    def EnemysMove(self):
        if (time.time()-self.enemyMoveInterval) > 0.2:
            for id, data in self.sv.gamescene.enemyData.items():
                self.EnemyPathRedirection(data)
                if data.pathData == None:
                    return
                self.PathProcess(data, time.time()-self.enemyMoveInterval)
            self.enemyMoveInterval = time.time()
        else:
            return

    def PathProcess(self, data, interval):
        if len(data.pathData) <= 0:
            return
        cell = data.pathData[-1]
        pos = self.sv.gamescene.mapData.GetRealWorldPosition(cell[0], cell[1])

        if time.time()-data.timeStamp > 5:
            data.speed = 4

        position = data.position
        dis = MathAuxiliary.Distance(pos, position)
        if dis > data.speed * interval:
            data.position = MathAuxiliary.Lerp(position, pos,  data.speed * interval).GetList()
        else:
            data.pathData.pop()
            data.position = pos

        for cid, uid in self.liveclients.items():
            msg = MsgSCMoveTo(data.entityID, -1, pos, 900)
            self.sv.host.sendClient(cid, msg.getPackedData())

        self.IsEnemyArrivalDesination(data)

    def IsEnemyArrivalDesination(self, enemyData):
        if enemyData.position[2] < self.destination[2]:
            self.DestroyEnemy(enemyData.entityID)
            self.sv.combatManager.EnemyArrival()

    def EnemyPathRedirection(self, enemyData):
        for uid,data in self.sv.gamescene.playerData.items():
            if MathAuxiliary.Distance(data.position, enemyData.position)<20:
                if data.userID != enemyData.targetID:
                    pathData = self.EnemyPathSolve(enemyData.entityID, data.position)
                    if pathData != None:
                        enemyData.pathData = pathData
                        enemyData.targetID = data.userID
            else:
                if enemyData.targetID == data.userID:
                    pathData = self.EnemyPathSolve(enemyData.entityID, self.destination)
                    enemyData.pathData = pathData
                    enemyData.targetID = -1



    def EnemyPathSolve(self, entityID, target):
        return self.sv.routerManager.NavigateTO(entityID, target)

    def RegisterLiveClient(self, host, cid, uid):
        self.liveclients[cid] = uid
        self.sv.gamescene.sendALLEnemies(host, cid)

    def UnregisterClient(self, cid):
        if self.liveclients.has_key(cid) == False:
            return

        self.liveclients.pop(cid)

    def FindEnemiesInCircle(self, pos, radius):
        retData = []
        for entityID,data in self.sv.gamescene.enemyData.items():
            if MathAuxiliary.Distance(pos, data.position) < radius:
                retData.append(data)

        return retData

    def EnemyAttack(self, host ,cid, msg):
        self.sv.combatManager.EnemyAttack(msg.entityID1, msg.entityID2)
