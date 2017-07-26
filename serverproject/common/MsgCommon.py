# -*- coding: GBK -*-
import struct
import conf
class MsgBase(object):
    def __init__(self):
        super(MsgBase, self).__init__()
        self.cid = -1

    def GetMsgCommand(self):
        return self.command

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
    def __init__(self, entityid, userID, movement):
        super(MsgSCMoveTo, self).__init__()
        self.command = conf.MSG_SC_MOVETO
        self.entityID = entityid
        self.movement = movement
        self.userID = userID

    def getPackedData(self):
        data = struct.pack('<iiifff', self.command, self.userID, self.entityID, self.movement[0], self.movement[1], self.movement[2])
        return data
