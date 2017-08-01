# -*- coding: GBK -*-

import sys
import time

from Services.UserServices import UserServices
from common import conf
from common import events
from common.dispatcher import Dispatcher
from common.header import Header
from network.simpleHost import SimpleHost


class Server(object):
    def __init__(self, host, port):
        super(Server, self).__init__()
        # Start host
        self.host = SimpleHost()
        self.host.startup(host, port)

        # login user dict
        self.login_user_map = {}
        # user room map
        self.user_room_map = {}

        # rooms
        self.rooms = []

        # Generate dispatcher
        self.dispatcher = Dispatcher()
        self.register_dispatcher_services()

        # map msg_type to message object
        self.msg_dict = None
        self.generate_msg_dict()

    def register_dispatcher_services(self):
        """
		Register services to dispatcher
		"""
        self.dispatcher.register(conf.USER_SERVICES, UserServices(self.host, self.login_user_map,
                                                                  self.rooms, self.user_room_map))

    def generate_msg_dict(self):
        """
		Map msg_type to message object
		"""
        self.msg_dict = {
            conf.MSG_REGISTER: events.MsgRegister(),
            conf.MSG_LOGIN: events.MsgLogin(),
            conf.MSG_LOGOUT: events.MsgLogout(),
            conf.MSG_CREATE_ROOM: events.MsgCreateRoom(),
            conf.MSG_JOIN_ROOM: events.MsgJoinRoom(),
            conf.MSG_LEAVE_ROOM: events.MsgLeaveRoom(),
            conf.MSG_START_GAME: events.MsgStartGame(),
        }

    def tick(self):
        # Try send and receive message
        self.host.process()
        # handle received message
        self.handle_received_msg()
        # update room status
        for room in self.rooms:
            if not room:
                continue
            room.tick()

    def handle_received_msg(self):
        """
		Handle received message from host
		"""
        try:
            # read message from host queue
            event, client_hid, data = self.host.read()
            if event == conf.NET_CONNECTION_DATA:
                # read client data
                msg_type = Header.get_htype_from_raw(data)[0]
                if msg_type in self.msg_dict:
                    msg = self.msg_dict[msg_type]
                    msg.unmarshal(data)
                    self.dispatcher.dispatch(msg, client_hid)
                else:
                    # message not register, let room handle it
                    if client_hid in self.user_room_map:
                        self.user_room_map[client_hid].handle_received_msg(msg_type, data, client_hid)
                    else:
                        print "handle received message error: client not in any room"
            elif event == conf.NET_CONNECTION_LEAVE:
                self.dispatcher.dispatch(self.msg_dict[conf.MSG_LOGOUT], client_hid)
        except:
            print "Handle received message error !!!!!!!!"


def main(sys_args):
    host = ""
    port = 34567
    # max_connect_num = 100
    # dbname = 'PlayData.db'
    # parser = argparse.ArgumentParser(description="Third Person Shooting Game Server")
    # parser.add_argument("-o", "--host", help="Host name")
    # parser.add_argument("-p", "--port", help="Server port")
    # parser.add_argument("-n", "--dbname", help="Player database name")
    # parser.add_argument("-u", "--connectnum", help="Maximum number of client connection")
    # args = parser.parse_args(args=sys_args)
    # if args.host:
    # 	host = args.host
    # if args.port:
    # 	port = int(args.port)
    # if args.dbname:
    # 	dbname = args.dbname
    # if args.connectnum:
    # 	max_connect_num = int(args.connectnum)

    # start game hall server
    # gh = GameServer(host, port, max_connect_num, dbname)
    # gh.run()
    server = Server(host, port)
    while True:
        server.tick()
        time.sleep(0.001)


if __name__ == '__main__':
    main(sys.argv[1:])
