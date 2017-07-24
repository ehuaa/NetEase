# -*- coding: GBK -*-
import struct

class MsgCSLogin(object):
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
            self.stat = 1
        except:
            self.stat = -1
            return

    def getPassword(self):
        if self.password != '':
            return self.password

    def getUsername(self):
        if self.userName != '':
            return self.userName

    def getStat(self):
        return self.stat