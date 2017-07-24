# -*- coding: GBK -*-

import sys
import cPickle
import time
import struct

sys.path.append('./common')

import conf

class SimpleServer(object):
    def __init__(self):
        super(SimpleServer, self).__init__()
        return

    def commondExtract(self, data):
        try:
            l,r = struct.unpack('<i6s', data)
        except:
            raise

        return l,r

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
