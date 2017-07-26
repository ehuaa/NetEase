import sys
import random

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')

from timer import TimerManager

class EnemyManager(object):
    def __init__(self, gameScene):
        super(EnemyManager, self).__init__()
        self.gamescene = gameScene
        self.liveclients = {}
        self.timerDelay = None
        self.timer = None
        self.count = 0
        self.spawn = False

    def _spawEnemy(self, number, host):
        enemyID = random.randint(1, 2)
        posx = random.random() * 30
        if random.randint(1,2) == 1:
            posx = -posx

        data = self.gamescene.CreateEnemy(enemyID, [posx,0,95])
        for k,v in self.liveclients.items():
            self.gamescene.SendEnemy(host, k, data)

        self.count += 1
        if self.count > number:
            self.timer.cancel()
            TimerManager.removeCancelledTasks()
            self.spawn = False

    def SpawnEnemy(self, interval, number ,host):
        self.timerDelay.cancel()
        TimerManager.removeCancelledTasks()
        self.timer = TimerManager.addRepeatTimer(interval, self._spawEnemy, number, host)


    #Handle the MSG_CS_ACTOR_ATTACK message
    def MsgHandler(self, host, cid, msg):
        pass

    # Update the enemies' state
    def Process(self, host):
        if len(self.liveclients) == 0:
            return

        TimerManager.scheduler()

        #spawn enemies and broadcast to all live clients
        if len(self.gamescene.enemyData) == 0 and self.spawn == False:
            self.timerDelay = TimerManager.addTimer(10, self.SpawnEnemy, 3, 20, host)
            self.count = 0
            self.spawn = True
        else: #Moving and attacking the Players
            pass

    def RegisterLiveClient(self, host, cid, uid):
        self.liveclients[cid] = uid
        self.gamescene.sendALLEnemies(host, cid)

    def UnregisterClient(self, cid):
         self.liveclients.pop(cid)