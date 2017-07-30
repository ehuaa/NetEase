# -*- coding: GBK -*-
import struct
import conf
class MsgBase(object):
    def __init__(self):
        super(MsgBase, self).__init__()
        self.command = -1
        self.params = []

    def GetMsgCommand(self):
        return self.command
    def GetIntValue(self,data):
        retVal = struct.unpack('<i', data[0:4])[0]
        data = data[4:]
        return retVal, data
    def GetFloatValue(self,data):
        retVal = struct.unpack('<f', data[0:4])[0]
        data = data[4:]
        return retVal, data
    def GetVector3Value(self,data):
        x,data = self.GetFloatValue(data)
        y,data = self.GetFloatValue(data)
        z,data = self.GetFloatValue(data)

        return [x,y,z],data

class MsgCSLogin(MsgBase):

    MSG_STAT_ERR = -1
    MSG_STAT_OK = 1

    def __init__(self, data):
        super(MsgCSLogin, self).__init__()
        self.command = conf.MSG_CS_LOGIN
        try:
            len = struct.unpack('<i',data[0:4])[0]
            data = data[4:]
            sub = data[0:len]
            self.userName = struct.unpack('<'+repr(len)+'s', sub)[0]

            data = data[len:]
            len = struct.unpack('<i', data[0:4])[0]
            data = data[4:]
            self.password = struct.unpack('<'+repr(len)+'s', data)[0]
            self.stat = self.MSG_STAT_OK
        except:
            self.stat = self.MSG_STAT_ERR
            return

    def getPassword(self):
        if self.password != '':
            return self.password

    def getUsername(self):
        if self.userName != '':
            return self.userName

    def getStat(self):
        return self.stat

class MsgSCConfirm(MsgBase):

    MSG_ERR_PROG = 1 # The client program err
    MSG_ERR_PW = 2 # The password or the userName is wrong
    MSG_OK = 0 # Login notify
    MSG_ERR_UNKNOWN = -1# Unknown err

    def __init__(self, uid = -1, msg = -1):
        super(MsgSCConfirm, self).__init__()
        self.userID = uid
        self.msgData = msg
        self.command = conf.MSG_SC_CONFIRM

    def getPackedData(self):
        return struct.pack('<iii',conf.MSG_SC_CONFIRM, self.userID, self.msgData)

class MsgCSAttack(MsgBase):

    WEAPON_ATTACK = 0
    MAGIC_ATTACK = 1
    ENEMY_NEAR = 2
    ENEMY_FAR = 3
    TRAP_BOOLD = 4
    TRAP_SPEED = 5

    def __init__(self, data):
        super(MsgCSAttack, self).__init__()
        self.command = conf.MSG_CS_ATTACK
        self.userID, data = self.GetIntValue(data)
        self.entityID1, data = self.GetIntValue(data)
        self.entityID2, data = self.GetIntValue(data)

        self.pos1,data = self.GetVector3Value(data)
        self.pos2,data = self.GetVector3Value(data)
        self.kind,data = self.GetIntValue(data)

class MsgCSEnemyAttack(MsgBase):
    def __init__(self, data):
        super(MsgCSEnemyAttack, self).__init__()
        self.command = conf.MSG_CS_ENEMY_ATTACK
        self.userID, data = self.GetIntValue(data)
        self.entityID1, data = self.GetIntValue(data)
        self.entityID2, data = self.GetIntValue(data)

class MsgCSTrapAttack(MsgBase):
    def __init__(self,data):
        super(MsgCSTrapAttack, self).__init__()
        self.command = conf.MSG_CS_TRAP_ATTACK
        self.userID, data = self.GetIntValue(data)
        self.entityID1, data = self.GetIntValue(data)
        self.entityID2, data = self.GetIntValue(data)

class MsgCSGameReplay(MsgBase):
    def __init__(self, data):
        self.command = conf.MSG_CS_GAME_REPLAY
        self.userID,data = self.GetIntValue(data)

class MsgCSTrapIn(MsgBase):
    def __init__(self,data):
        self.command = conf.MSG_CS_TRAP_IN
        self.userID, data = self.GetIntValue(data)
        self.trapID, data = self.GetIntValue(data)
        self.position,data = self.GetVector3Value(data)

class MsgCSBuy(MsgBase):
    def __init__(self, data):
        self.command = conf.MSG_CS_BUY
        self.userID, data = self.GetIntValue(data)
        self.trapID, data = self.GetIntValue(data)

class MsgSCLoadscene(MsgBase):
    MSG_KIND_PLAYER = 0
    MSG_KIND_ENEMY = 1
    MSG_KIND_TRAP = 2

    def __init__(self,kind = 0, uid =-1, position=[0.0,0.0,0.0],q = [1.0, 0.0, 0.0, 0.0],entityid = -1):
        super(MsgSCLoadscene, self).__init__()
        self.command = conf.MSG_SC_SCENE_LOAD
        self.kind = kind
        self.ID = uid
        self.entityID = entityid
        self.pos = position
        self.quat = q

    def getPackedData(self):

        data = struct.pack('<iiiifffffff', conf.MSG_SC_SCENE_LOAD, self.kind, self.ID, self.entityID,self.pos[0], self.pos[1], self.pos[2], self.quat[0], self.quat[1], self.quat[2], self.quat[3])

        return data

class MsgCSMoveTo(MsgBase):
    MSG_ERR = -1
    MSG_OK = 0

    def __init__(self, data):
        super(MsgCSMoveTo, self).__init__()
        self.command = conf.MSG_CS_MOVETO
        try:
            self.userID = struct.unpack('<i', data[0:4])[0]
            data = data[4:]
            sub = data[0:4]
            self.x = struct.unpack('<f', sub)[0]
            data = data[4:]
            sub = data[0:4]
            self.y = struct.unpack('<f', sub)[0]
            data = data[4:]
            sub = data[0:4]
            self.z = struct.unpack('<f', sub)[0]
            self.stat = self.MSG_OK
        except:
            self.stat = self.MSG_ERR

    def GetUserID(self):
        return self.userID

    def GetMovement(self):
        return [self.x, self.y, self.z]

class MsgSCMoveTo(MsgBase):
    def __init__(self, entityid, userID, movement, speed = 300):
        super(MsgSCMoveTo, self).__init__()
        self.command = conf.MSG_SC_MOVETO
        self.entityID = entityid
        self.movement = movement
        self.userID = userID
        self.speed = speed

    def getPackedData(self):
        data = struct.pack('<iiiffff', self.command, self.userID, self.entityID, self.movement[0], self.movement[1], self.movement[2], self.speed)
        return data

class MsgSCEnemyDie(MsgBase):
    def __init__(self, entityID):
        super(MsgSCEnemyDie, self).__init__()
        self.command = conf.MSG_SC_ENEMY_DIE
        self.entityID = entityID

    def getPackedData(self):
        data = struct.pack('<ii', self.command, self.entityID)
        return data

class MsgSCPlayerAttack(MsgBase):

    WEAPON_ATTACK = 0
    MAGIC_ATTACK = 1
    ENEMY_NEAR = 2
    ENEMY_FAR = 3
    TRAP_BOOLD = 4
    TRAP_SPEED = 5

    def __init__(self, UserID, EntityID, Kind):
        self.command = conf.MSG_SC_PLAYER_ATTACK
        self.userID = UserID
        self.entityID = EntityID
        self.kind = Kind

    def getPackedData(self):
        data = struct.pack('<iiii', self.command, self.userID, self.entityID, self.kind)
        return data

class MsgSCPlayerLogout(MsgBase):
    def __init__(self, UserID, EntityID):
        self.command = conf.MSG_SC_PLAYER_LOGOUT
        self.userID = UserID
        self.entityID = EntityID

    def getPackedData(self):
        data = struct.pack('<iii', self.command, self.userID, self.entityID)
        return data

class MsgSCMoney(MsgBase):
    def __init__(self, UserID, Money):
        self.command = conf.MSG_SC_MONEY
        self.userID = UserID
        self.money = Money

    def getPackedData(self):
        data = struct.pack('<iii', self.command, self.userID, self.money)
        return data

class MsgSCGameOver(MsgBase):
    def __init__(self):
        self.command = conf.MSG_SC_GAME_OVER

    def getPackedData(self):
        data = struct.pack('<i', self.command)
        return data

class MsgSSGameOver(MsgBase):
    def __init__(self):
        self.command = conf.MSG_SS_GAME_OVER

class MsgSCGameWin(MsgBase):
    def __init__(self):
        self.command = conf.MSG_SC_GAME_WIN

    def getPackedData(self):
        data = struct.pack('<i', self.command)
        return data

class MsgSCBlood(MsgBase):
    def __init__(self, UserID, Blood):
        super(MsgBase, self).__init__()
        self.command = conf.MSG_SC_PLAYER_BLOOD
        self.userID = UserID
        self.blood=Blood

    def getPackedData(self):
        data = struct.pack("<iii", self.command, self.userID, self.blood)
        return data

class MsgSCPlayerDie(MsgBase):
    def __init__(self,UserID):
        super(MsgBase, self).__init__()
        self.command = conf.MSG_SC_PLAYER_DIE
        self.userID = UserID

    def getPackedData(self):
        data = struct.pack("<ii", self.command, self.userID)
        return data

class MsgSCBackpack(MsgBase):
    def __init__(self, TrapID1, Num1, TrapID2, Num2):
        super(MsgBase, self).__init__()
        self.command = conf.MSG_SC_BACKPACK
        self.trapID1 = TrapID1
        self.trapID2 = TrapID2
        self.num1 = Num1
        self.num2 = Num2

    def getPackedData(self):
        data = struct.pack("<iiiii", self.command, self.trapID1, self.num1, self.trapID2, self.num2)
        return data

class MsgSCTrapDie(MsgBase):
    def __init__(self, entityid):
        self.command=conf.MSG_SC_TRAP_DIE
        self.entiyID = entityid

    def getPackedData(self):
        data = struct.pack("<ii", self.command, self.entiyID)
        return data