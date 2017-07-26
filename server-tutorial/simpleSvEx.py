# -*- coding: GBK -*-

import sys
import time
import struct

sys.path.append('./common')
sys.path.append('./network')
sys.path.append('./database')

import conf
from simpleHost import SimpleHost
from MsgCommon import MsgCSLogin,MsgSCConfirm
from login import LoginServer
from gameScene import GameScene

class SimpleServer(object):
    def __init__(self):
        super(SimpleServer, self).__init__()
        self.host = SimpleHost()
        self.loginServer = LoginServer()
        self.gameScene = GameScene()

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
                msg = self.commondExtract(data);

                if type(msg) is MsgCSLogin:
                    self.LoginProcedure(msg, wparam)


                #self.host.closeClient(wparam)
                #self.host.shutdown()

            elif event == conf.NET_CONNECTION_LEAVE:
                pass
                #Save Data into the database
            elif event == conf.NET_CONNECTION_NEW:
                pass
                #Idle

    def LoginProcedure(self, msg, cid):
        retMsg = MsgSCConfirm()
        if msg.getStat() == msg.MSG_STAT_OK:
            stat, userID = self.loginServer.userPasswordConfirm(msg.getUsername(), msg.getPassword())
            if  stat == 1:
                retMsg.msgData = retMsg.MSG_OK
                retMsg.userID = userID
            else:
                retMsg.msgData = retMsg.MSG_ERR_PW
        else:
            retMsg.msgData = retMsg.MSG_ERR_PROG

        data = retMsg.getPackedData()
        self.host.sendClient(cid, data)

        self.SendingMainSceneData(cid,retMsg)

    #Sending scene data to the client
    def SendingMainSceneData(self, cid, retMsg):
        if retMsg.msgData == retMsg.MSG_OK:
            self.gameScene.SendAllObj(self.host, cid, retMsg.userID)
            return





if __name__=="__main__":
    testserver = SimpleServer()
    testserver.startServer()
