import sys

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')

from common.math3d import MathAuxiliary
from managerbase import ManagerBase

class RouteManager(ManagerBase):
    def __init__(self, sv):
        super(RouteManager, self).__init__()
        self.sv = sv

    def MovePermission(self, entityID, move):
        data = self.sv.gamescene.GetEntityData(entityID)
        pos = data.position

        newpos = MathAuxiliary.AddVector3(move, pos)

        bmask = self.sv.gamescene.mapData.GetMaskData(newpos)

        if bmask == 1:
            return False
        else:
            return True

    def NavigateTO(self, entityID, pos):
        start = self.sv.gamescene.GetEntityData(entityID).position
        return self.sv.gamescene.mapData.FindPathToPostion(start, pos)

    #Enemy path solving
    def Process(self, host):
        pass

