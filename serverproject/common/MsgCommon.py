# -*- coding: GBK -*-
import struct
import conf

class MsgCSLogin(object):

    MSG_STAT_ERR = -1
    MSG_STAT_OK = 1

    def __init__(self, data):
        super(MsgCSLogin, self).__init__()
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


class MsgSCConfirm(object):

    MSG_ERR_PROG = 1 # The client program err
    MSG_ERR_PW = 2 # The password or the userName is wrong
    MSG_OK = 0 # Login notify
    MSG_ERR_UNKNOWN = -1# Unknown err

    def __init__(self, uid = -1, msg = -1):
        super(MsgSCConfirm, self).__init__()
        self.userID = uid
        self.msgData = msg

    def getPackedData(self):
        return struct.pack('<iii',conf.MSG_SC_CONFIRM, self.userID, self.msgData)

class MsgSCLoadscene(object):
    MSG_KIND_PLAYER = 0
    MSG_KIND_ENEMY = 1
    MSG_KIND_TRAP = 2

    def __init__(self,kind = 0, uid =-1, position=[0.0,0.0,0.0],q = [1.0, 0.0, 0.0, 0.0],entityid = -1):
        super(MsgSCLoadscene, self).__init__()
        self.kind = kind
        self.ID = uid
        self.entityID = entityid
        self.pos = position
        self.quat = q

    def getPackedData(self):

        data = struct.pack('<iiiifffffff', conf.MSG_SC_SCENE_LOAD, self.kind, self.ID, self.entityID,self.pos[0], self.pos[1], self.pos[2], self.quat[0], self.quat[1], self.quat[2], self.quat[3])

        return data

