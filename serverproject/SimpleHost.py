# -*- coding: GBK -*-

import sys
import cPickle
import time
import struct

sys.path.append('./common')
sys.path.append('./network')

import conf
from simpleHost import SimpleHost
from MsgCommon import MsgCSLogin

class SimpleServer(object):
    def __init__(self):
        super(SimpleServer, self).__init__()
        self.host = SimpleHost()
        return

    def commondExtract(self, data):
        try:
            cm = data[0:4]
            cmdcode = struct.unpack('<i', cm)[0]

            if cmdcode == conf.MSG_CS_LOGIN:
                msg = MsgCSLogin(data[4:])
                return msg
            elif cmdcode == conf.MSG_CS_LOGOUT:
                return None

        except:
            return None

    def startServer(self):
        
        self.host.startup('127.0.0.1', 5001)

        while 1:
            time.sleep(0.1)
            self.host.process()

            event, wparam, data = self.host.read()

            if event < 0:
                continue

            if event == conf.NET_CONNECTION_DATA:
                self.host.sendClient(wparam, 'RE: ' + "sai I know you")

                client_stat, message=self.commondExtract(data);

                if client_stat == 1:
                    print message

                elif client_stat == 2:
                    self.host.closeClient(wparam)
                    self.host.shutdown()
                    break

if __name__=="__main__":
    testserver = SimpleServer()
    testserver.startServer()
