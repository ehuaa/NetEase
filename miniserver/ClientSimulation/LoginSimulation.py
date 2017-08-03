from common import conf
from common.events import MsgCSLogin
from network.netStream import NetStream

head = MsgCSLogin('test', "sdskk")
data = head.marshal()
sock = NetStream()
sock.connect('127.0.0.1', 2000)
if sock.status() == conf.NET_STATE_ESTABLISHED:
    sock.send(data)