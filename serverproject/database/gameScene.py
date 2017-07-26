# -*- coding: GBK -*-
import sys

sys.path.append('../common')
sys.path.append('../gameservice')

from actorAttributes import ActorAttributes
from enemyAttr import EnemyAttributes
from trapAttr import TrapAttributes
from MsgCommon import MsgSCLoadscene
from router import RouteManager
from combat import CombatManager

class GameScene(object):
    def __init__(self):
        super(GameScene, self).__init__()
        self.playerpath = './database/gamescenePlayer.txt'
        self.enemypath = './database/gamesceneEnemy.txt'
        self.trappath = './database/gamesceneTrap.txt'
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

        self._savePlayers("")#Test
        self.routerManager = RouteManager(self)
        self.combarManager = CombatManager(self)

        return
    def _initEntityData(self):
        for k,val in self.playerData.items():
            self.EntityIDS[val['EntityID']] = val
        for k, val in self.enemyData.items():
            self.EntityIDS[val['EntityID']] = val
        for k, val in self.trapData.items():
            self.EntityIDS[val['EntityID']] = val

    def _savePlayers(self, path):
        f = open("playerTest.txt", 'w')
        try:
            for k,val in self.playerData.items():
                self._savePlayer(f, val)
                f.write('\n')
            f.close()
        except:
            f.close()

    def _savePlayer(self, f, d):
        for k,val in d.items():
            if type(val) == dict:
                line = repr(k) + ":{" + self._getsubDict(val) + "}\n"
            else:
                line = repr(k) + ":" + repr(val) + '\n'

            f.write(line)

    def _getsubDict(self, d):
        line = ""
        for k,val in d.items():
            sub = repr(k)+":"+repr(val)+','
            line+=sub
        return line[0:-1]

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
                        self.playerData[data['EntityID']] = data
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value

            if len(data) != 0:
                self.playerData[data['UserID']] = data

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
                        self.enemyData[data['EntityID']] = data
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value
            if len(data) != 0:
                self.enemyData[data['EntityID']] = data

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
                        self.trapData[data['Entity']] = data
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value
            if len(data) != 0:
                self.trapData[data['EntityID']] = data

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

                data[key] = float(value)

            key, value = self._getKeyValue(str)
            data[key] = float(value)

            return data
        except:
            raise

    def getPlayerData(self, userID):
        try:
            return self.playerData[userID]
        except:
            return None

    def getEnemyData(self, EntityID):
        try:
            return self.enemyData[EntityID]
        except:
            return None

    def getTrapData(self, EntityID):
        try:
            return self.trapData[EntityID]
        except:
            return None

    def SendAllObj(self, host, cid, userID):
        self.sendAllTraps(host, cid)

    #Init blood and money and backpack
    def initPlayerAttr(self, host, cid, userID):
        pass

    def sendAllPlayers(self, host, cid, userID):

        if self.playerData.has_key(repr(userID)) == False:
            entityID = self.GenerateEntityID()
            data ={'UserID':userID, 'position':{'x':0, 'y':0, 'z':0}, 'quat':{'w':1,'x':0, 'y':0, 'z':0}, 'EntityID':entityID}
            self.AddPlayer(entityID, data)

        for k,val in self.playerData.items():
            userID = int(val['UserID'])
            pos = self._getposition(val['position'])
            q = self._getQuat(val['quat'])
            entityID = int(val['EntityID'])

            msg = MsgSCLoadscene(MsgSCLoadscene.MSG_KIND_PLAYER, userID, pos, q, entityID)
            data = msg.getPackedData()

            host.sendClient(cid, data)

    def sendALLEnemies(self, host, cid):
        for k, val in self.enemyData.items():
            enemyID = int(val['EnemyID'])
            entityID = int(val['EntityID'])
            pos = self._getposition(val['position'])
            q = self._getQuat(val['quat'])

            msg = MsgSCLoadscene(MsgSCLoadscene.MSG_KIND_ENEMY, enemyID, pos, q, entityID)
            data = msg.getPackedData()

            host.sendClient(cid, data)

    def sendAllTraps(self, host, cid):
        for k, val in self.trapData.items():
            trapID = int(val['TrapID'])
            entityID = int(val['EntityID'])
            pos = self._getposition(val['position'])
            q = self._getQuat(val['quat'])

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
            if self.EntityIDS.has_key(repr(id)) == False:
                return id

    def AddEnemy(self, entityID, data):
        self.enemyData[repr(entityID)] = data
        self.EntityIDS[repr(entityID)] = data

    def AddPlayer(self, entityID, data):
        self.playerData[repr(entityID)] = data
        self.EntityIDS[repr(entityID)] = data

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

        self.AddEnemy(entityid, data)

        return data

    def SendEnemy(self, host, cid, val):
        enemyID = int(val['EnemyID'])
        entityID = int(val['EntityID'])
        pos = self._getposition(val['position'])
        q = self._getQuat(val['quat'])

        msg = MsgSCLoadscene(MsgSCLoadscene.MSG_KIND_ENEMY, enemyID, pos, q, entityID)
        data = msg.getPackedData()

        host.sendClient(cid, data)