# -*- coding: GBK -*-

import sys
import time
import struct

sys.path.append('./common')
sys.path.append('./network')
sys.path.append('./database')
sys.path.append('./gameservice')

import conf
from simpleHost import SimpleHost
from MsgCommon import MsgCSLogin,MsgSCConfirm,MsgCSMoveTo
from login import LoginServer
from gameScene import GameScene
from dispatcher import Dispatcher
from enemymanager import EnemyManager
from playermanager import PlayerManager

class SimpleServer(object):
    def __init__(self):
        super(SimpleServer, self).__init__()
        self.host = SimpleHost()
        self.gameScene = GameScene()
        self.loginServer = LoginServer()
        self.dispatch = Dispatcher()
        self.entities = {}
        self.messageHandler = {}
        self._initmessagehandler()

        self.enemyManager = EnemyManager(self.gameScene)
        self.playerManager = PlayerManager(self.gameScene)

        self.RegisterMessageHandler(conf.MSG_CS_MOVETO, self.playerManager.MsgHandler)

        return
    def RegisterMessageHandler(self, msgCommond, func):
        self.messageHandler[msgCommond].append(func)

    def UnRegisterMessageHandler(self, msgCommond, func):
        self.messageHandler[msgCommond].remove(func)

    def _initmessagehandler(self):
        self.messageHandler[conf.MSG_CS_LOGIN]=[]
        self.messageHandler[conf.MSG_CS_LOGOUT]=[]
        self.messageHandler[conf.MSG_CS_MOVETO]=[]
        self.messageHandler[conf.MSG_CS_ACTOR_ATTACK]=[]
        self.messageHandler[conf.MSG_CS_ENEMY_ATTACK]=[]
        self.messageHandler[conf.MSG_CS_WEAPON_UPGRADE]=[]
        self.messageHandler[conf.MSG_CS_MONEY]=[]
        self.messageHandler[conf.MSG_CS_WEAPON_ATTACK]=[]

    def generateEntityID(self):
        raise NotImplementedError

    def registerEntity(self, entity):
        eid = self.generateEntityID
        entity.id = eid

        self.entities[eid] = entity

        return

    def commondExtract(self, data):
        try:
            cm = data[0:4]
            cmdcode = struct.unpack('<i', cm)[0]

            if cmdcode == conf.MSG_CS_LOGIN:
                msg = MsgCSLogin(data[4:])
                return msg
            elif cmdcode == conf.MSG_CS_MOVETO:
                msg = MsgCSMoveTo(data[4:])
                return msg

        except:
            return None

    def msgProcess(self, handlers, cid, msg):
        for hd in handlers:
            hd(self.host, cid, msg)


    def startServer(self):
        
        self.host.startup('127.0.0.1', 5001)

        while 1:
            #time.sleep(0.1)
            self.host.process()
            self.enemyManager.Process(self.host)
            self.playerManager.Process(self.host)

            event, wparam, data = self.host.read()

            if event < 0:
                continue

            if event == conf.NET_CONNECTION_DATA:
                msg = self.commondExtract(data);
                msg.cid = wparam

                if type(msg) is MsgCSLogin:
                    retval,userID = self.LoginProcedure(self.host, msg, wparam)
                    if retval == True:
                        self.playerManager.RegisterLiveClient(self.host, wparam, userID)
                        self.enemyManager.RegisterLiveClient(self.host, wparam, userID)
                else:
                    self.msgProcess(self.messageHandler[msg.GetMsgCommand()], wparam, msg)

                #self.host.closeClient(wparam)
                #self.host.shutdown()

            elif event == conf.NET_CONNECTION_LEAVE:
                pass
                #Save Data into the database

            elif event == conf.NET_CONNECTION_NEW:
                pass
                #Idle

    def LoginProcedure(self, host, msg, cid):
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
        host.sendClient(cid, data)

        if retMsg.msgData == retMsg.MSG_OK:
            self.gameScene.SendAllObj(host, cid, retMsg.userID)
            return True,retMsg.userID

        return False,retMsg.userID

if __name__=="__main__":
    testserver = SimpleServer()
    testserver.startServer()
