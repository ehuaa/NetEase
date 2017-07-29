# -*- coding: GBK -*-
import sys

sys.path.append('../common')
sys.path.append('../gameservice')

from actorAttributes import ActorAttributes
from enemyAttr import EnemyAttributes
from trapAttr import TrapAttributes
from MsgCommon import MsgSCLoadscene
from mapdata import MapData

class DataBase(object):
    def __init__(self):
        super(DataBase, self).__init__()

    def GetVector3(self,data):
        x = float(data['x'])
        y = float(data['y'])
        z = float(data['z'])
        return [x,y,z]

    def GetQuat(self,data):
        w = float(data['w'])
        x = float(data['x'])
        y = float(data['y'])
        z = float(data['z'])

        return [w,x,y,z]

class UserData(DataBase):
    def __init__(self,data=None):
        super(UserData, self).__init__()
        if data == None:
            return
        self.userID = int(data['UserID'])
        self.entityID = int(data['EntityID'])
        self.position = self.GetVector3(data['position'])
        self.quat = self.GetQuat(data['quat'])
        self.dead = False

class EnemyData(DataBase):
    def __init__(self,data):
        super(EnemyData, self).__init__()
        self.enemyID = int(data['EnemyID'])
        self.entityID = int(data['EntityID'])
        self.position = self.GetVector3(data['position'])
        self.quat = self.GetQuat(data['quat'])
        self.blood = int(data['blood'])
        self.speed = 300
        self.pathData = None
        self.targetEntityID = None

class TrapData(DataBase):
    def __init__(self,data):
        super(TrapData, self).__init__()
        self.trapID = int(data['TrapID'])
        self.entityID = int(data['EntityID'])
        self.position = self.GetVector3(data['position'])
        self.quat = self.GetQuat(data['quat'])

class GameScene(object):
    def __init__(self):
        super(GameScene, self).__init__()
        self.playerpath = './database/gamescenePlayer.txt'
        self.enemypath = './database/gamesceneEnemy.txt'
        self.trappath = './database/gamesceneTrap.txt'

        self.mapData = MapData()
        self.playerData = {}
        self.enemyData = {}
        self.trapData = {}

        self._loadPlayer(self.playerpath)
        self._loadEnemy(self.enemypath)
        self._loadTrap(self.trappath)

        self.actor_attr = ActorAttributes()
        self.enemy_attr = EnemyAttributes()
        self.trap_attr = TrapAttributes()

        self.gamestage = 0

        self.EntityIDS={}
        self._initEntityData()

        return

    def _initEntityData(self):
        for k,val in self.playerData.items():
            self.EntityIDS[val.entityID] = val
        for k, val in self.enemyData.items():
            self.EntityIDS[val.entityID] = val
        for k, val in self.trapData.items():
            self.EntityIDS[val.entityID] = val

    def _loadPlayer(self, path):
        f = open(path, 'r')

        try:
            data = {}
            for line in f:
                if line == '\n' or line == '':
                    continue

                key, value = self._getKeyValue(line[0:-1])

                if key == 'UserID':
                    if len(data) != 0:
                        cell = UserData(data)
                        self.playerData[cell.userID] = cell
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value

            if len(data) != 0:
                cell = UserData(data)
                self.playerData[cell.userID] = cell

            f.close()

        except:
            f.close()
            raise

    def _loadEnemy(self, path):
        f = open(path, 'r')

        try:
            data = {}
            for line in f:
                if line == '\n' or line == '':
                    continue

                key, value = self._getKeyValue(line[0:-1])

                if key == 'EnemyID':
                    if len(data) != 0:
                        cell = EnemyData(data)
                        self.enemyData[cell.entityID] = cell
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value
            if len(data) != 0:
                cell = EnemyData(data)
                self.enemyData[cell.entityID] = cell

            f.close()

        except:
            f.close()
            raise

    def _loadTrap(self, path):
        f = open(path, 'r')

        try:
            data = {}
            for line in f:
                if line == '\n' or line == '':
                    continue

                key, value = self._getKeyValue(line[0:-1])

                if key == 'TrapID':
                    if len(data) != 0:
                        cell = TrapData(data)
                        self.trapData[cell.entityID] = cell
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value
            if len(data) != 0:
                cell = TrapData(data)
                self.trapData[cell.entityID] = cell

            f.close()

        except:
            f.close()
            raise

    def _getKeyValue(self, str):
        try:
            pos = str.index(':')
            key = str[0:pos]
            value = str[pos + 1:]

            if value[0] == '{':
                value = self._parsePosition(value)

            return key, value
        except:
            raise

    def _parsePosition(self, str):
        str = str.strip('{}')
        data = {}
        try:
            index = str.find(',')
            while index != -1:
                key, value = self._getKeyValue(str[0:index])
                str = str[index + 1:]
                index = str.find(',')

                data[key] = value

            key, value = self._getKeyValue(str)
            data[key] = value

            return data
        except:
            raise

    def GetPlayerData(self, userID):
        try:
            return self.playerData[userID]
        except:
            return None

    def GetEnemyData(self, EntityID):
        try:
            return self.enemyData[EntityID]
        except:
            return None

    def GetTrapData(self, EntityID):
        try:
            return self.trapData[EntityID]
        except:
            return None

    def GetEntityData(self, entityID):
        try:
            return self.EntityIDS[entityID]
        except:
            return None

    #Init blood and money and backpack
    def initPlayerAttr(self, host, cid, userID):
        pass

    def CreateUserData(self, userID):
        entityID = self.GenerateEntityID()

        cell = UserData()
        cell.userID = userID
        cell.entityID = entityID
        cell.position = [0,0,0]
        cell.quat = [1,0,0,0]

        self.AddPlayer(cell)

        return cell

    def sendALLEnemies(self, host, cid):
        for k, val in self.enemyData.items():
            enemyID = val.enemyID
            entityID = val.entityID
            pos = val.position
            q = val.quat

            msg = MsgSCLoadscene(MsgSCLoadscene.MSG_KIND_ENEMY, enemyID, pos, q, entityID)
            data = msg.getPackedData()

            host.sendClient(cid, data)

    def sendAllTraps(self, host, cid):
        for k, val in self.trapData.items():
            trapID = val.trapID
            entityID = val.entityID
            pos = val.position
            q = val.quat

            msg = MsgSCLoadscene(MsgSCLoadscene.MSG_KIND_TRAP, trapID, pos, q, entityID)
            data = msg.getPackedData()

            host.sendClient(cid, data)

    def _getposition(self, d):
        retVal = []
        retVal.append(float(d['x']))
        retVal.append(float(d['y']))
        retVal.append(float(d['z']))
        return retVal

    def _getQuat(self, d):
        retVal = []
        retVal.append(float(d['w']))
        retVal.append(float(d['x']))
        retVal.append(float(d['y']))
        retVal.append(float(d['z']))
        return retVal

    def GenerateEntityID(self):
        for id in xrange(1, len(self.EntityIDS)+2):
            if self.EntityIDS.has_key(id) == False:
                return id

    def AddEnemy(self, entityID, data):
        self.enemyData[data.entityID] = data
        self.EntityIDS[data.entityID] = data

    def AddPlayer(self, data):
        self.playerData[data.userID] = data
        self.EntityIDS[data.entityID] = data

    def AddTrap(self, entityID, data):
        self.trapData[repr(entityID)] = data
        self.EntityIDS[repr(entityID)] = data

    def CreateEnemy(self, enemyid, pos = [0, 0, 95], quat = [1, 0, 0, 0]):
        entityid = self.GenerateEntityID()
        data = {}
        data["EnemyID"] = repr(enemyid)
        data['EntityID'] = repr(entityid)
        data['blood'] = repr(100)
        data['quat'] = {'w':quat[0], 'x':quat[1], 'y':quat[2], 'z':quat[3]}
        data['position'] = {'x':pos[0], 'y':pos[1], 'z':pos[2]}

        data = EnemyData(data)
        self.AddEnemy(entityid, data)

        return data

    def DestroyEnemy(self, entityID):
        self.enemyData.pop(entityID)
        self.EntityIDS.pop(entityID)

    def DestroyAllEnemy(self):
        for key, val in self.enemyData.items():
            self.DestroyEnemy(val.entityID)

    def SendEnemy(self, host, cid, val):
        enemyID = val.enemyID
        entityID = val.entityID
        pos = val.position
        q = val.quat

        msg = MsgSCLoadscene(MsgSCLoadscene.MSG_KIND_ENEMY, enemyID, pos, q, entityID)
        data = msg.getPackedData()

        host.sendClient(cid, data)