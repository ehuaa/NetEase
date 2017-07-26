import sys

sys.path.append('./common')
sys.path.append('./common_server')
sys.path.append('./database')

class RouteManager(object):
    def __init__(self, gameScene):
        super(RouteManager, self).__init__()
        self.gamescene = gameScene

    def MovePermission(self, entityID, move):
        return True

    def NavigateTO(self, entityID, pos):
        pass

