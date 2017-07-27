import sys

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')

class CombatManager(object):
    def __init__(self, sv):
        super(CombatManager, self).__init__()
        self.sv = sv
        self.liveclients = {}

    def PlayerFireLight(self,msg):
        # Not Implemented (Is it a legal attack?)

        data = self.sv.gamescene.getEnemyData(msg.entityID2)

        if data == None:
            return

        blood = int(data['blood'])
        blood = blood - 10

        if blood <= 0:
            blood = 0
            data['blood']= repr(blood)
            self.sv.enemyManager.DestroyEnemy(msg.entityID2)
        else:
            data['blood']= repr(blood)


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