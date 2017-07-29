import sys
import random

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')

from datetime import datetime
from managerbase import ManagerBase

from timer import TimerManager
from MsgCommon import MsgSCEnemyDie,MsgSCMoveTo,MsgSSGameOver
import conf

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
        self.enemyMoveInterval = datetime.now()


    def _initMsgHandlers(self):
        self.msgHandlers[conf.MSG_SS_GAME_OVER] = []
        self.msgHandlers[conf.MSG_CS_GAME_REPLAY] = []
        self._registerMsgHandler(conf.MSG_SS_GAME_OVER, self.GameOver)
        self._registerMsgHandler(conf.MSG_CS_GAME_REPLAY, self.GameReplay)

    def GameReplay(self, host,cid ,msg):
        if self.timerDelay != None:
            self.timerDelay.cancel()

        if self.timer != None:
            self.timer.cancel()

        self.timerDelay = None
        self.timer = None
        self.count = 0
        self.spawn = False
        self.destination = [0, 0, -70]
        self.enemyMoveInterval = datetime.now()
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
        if (datetime.now()-self.enemyMoveInterval).microseconds/1000 > 900:
            for id, data in self.sv.gamescene.enemyData.items():
                self.EnemyPathRedirection(data)
                if data.pathData == None:
                    return

                try:
                    cell = data.pathData.pop()
                except:
                    cell = None

                if cell != None:
                    pos = self.sv.gamescene.mapData.GetRealWorldPosition(cell[0], cell[1])
                    data.position = pos
                    for cid,uid in self.liveclients.items():
                        msg = MsgSCMoveTo(data.entityID, -1, pos, 900)
                        self.sv.host.sendClient(cid, msg.getPackedData())

                    self.IsEnemyArrivalDesination(data)

            self.enemyMoveInterval = datetime.now()
        else:
            return

    def IsEnemyArrivalDesination(self, enemyData):
        if enemyData.position[2]<self.destination[2]:
            self.DestroyEnemy(enemyData.entityID)
            self.sv.combatManager.EnemyArrival()

    def EnemyPathRedirection(self, enemyData):
        pass

    def EnemyPathSolve(self, entityID, target):
        return self.sv.routerManager.NavigateTO(entityID, target)

    def RegisterLiveClient(self, host, cid, uid):
        self.liveclients[cid] = uid
        self.sv.gamescene.sendALLEnemies(host, cid)

    def UnregisterClient(self, cid):
        if self.liveclients.has_key(cid) == False:
            return

        self.liveclients.pop(cid)