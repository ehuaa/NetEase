from common import conf
from common.events import MsgCSLogin,MsgCSPlayerMove,MsgSCRoommateAdd,MsgSCRoommateDel
from network.netStream import NetStream
from common.header import Header
import time

if __name__=="__main__":
    head = MsgCSLogin('client1', "163")
    data = head.marshal()
    sock = NetStream()
    sock.connect('127.0.0.1', 2000)

    sock.nodelay(1)
    confirm = False
    gamestarted = False
    playerborn = False

    while(1):
        time.sleep(0.3)
        sock.process()
        if sock.status() == conf.NET_STATE_ESTABLISHED:
            if confirm == False:
                sock.send(data)
                confirm = True

            data = sock.recv()
            if data:
                msg_type = Header.get_htype_from_raw(data)[0]
                if msg_type == conf.MSG_SC_LOGIN_RESULT:
                    print "Login returned"
                elif msg_type == conf.MSG_SC_START_GAME:
                    gamestarted = True
                    print "Game Started"
                elif msg_type == conf.MSG_SC_ROOMMATE_ADD:
                    msg = MsgSCRoommateAdd("")
                    msg.unmarshal(data)
                    print msg.username
                elif msg_type == conf.MSG_SC_ROOMMATE_DEL:
                    msg = MsgSCRoommateAdd("")
                    msg.unmarshal(data)
                    print msg.username
                elif msg_type == conf.MSG_SC_PLAYER_BORN:
                    playerborn = True
                    print "Player Born"

            if gamestarted and playerborn:
                import  random
                msg = MsgCSPlayerMove(-1, 0.0, random.random(), 0.0, 0.0,0.0,0.0)
                data = msg.marshal()
                sock.send(data)




