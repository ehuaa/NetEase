import sys

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')

class CombatManager(object):
    def __init__(self, gameScene):
        super(CombatManager, self).__init__()
        self.gamescene = gameScene
        self.liveclients = {}

    def PlayerFireLight(self, userID, direct):
        pass

    def PlayerFireArea(self, userID, direct):
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