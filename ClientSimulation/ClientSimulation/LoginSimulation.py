from common import conf
from common.events import MsgCSLogin
from network.netStream import NetStream


if __name__=="__main__":
    head = MsgCSLogin('test', "sdskk")
    data = head.marshal()
    sock = NetStream()
    sock.connect('127.0.0.1', 2000)

    sock.nodelay(1)

    while(1):
        sock.process()
        if sock.status() == conf.NET_STATE_ESTABLISHED:
            sock.send(data)