# -*- coding: GBK -*-

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
        self.dispatcher.register(conf.USER_SERVICES, UserServices(self.host, self.login_user_map,
                                                                  self.rooms, self.user_room_map))
        # register MatchServices

    def generate_msg_dict(self):
        self.msg_dict = {
            conf.MSG_CS_REGISTER: events.MsgCSRegister(),
            conf.MSG_CS_LOGIN: events.MsgCSLogin(),
            conf.MSG_CS_LOGOUT: events.MsgCSLogout()
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
        try:
            # read message from host queue
            event, client_hid, data = self.host.read()

            if event == conf.NET_CONNECTION_DATA:
                # read client data
                msg_type = Header.get_htype_from_raw(data)[0]
                if msg_type in self.msg_dict:
                    msg = self.msg_dict[msg_type]
                    msg.unmarshal(data)
                    # Dispatch message
                    self.dispatcher.dispatch(msg, client_hid)
                else:
                    # message not register, let room handle it
                    if client_hid in self.user_room_map:
                        self.user_room_map[client_hid].handle_received_msg(msg_type, data, client_hid)
                    else:
                        print "handle received message error: client not in any room"
            elif event == conf.NET_CONNECTION_LEAVE:
                self.dispatcher.dispatch(self.msg_dict[conf.MSG_CS_LOGOUT], client_hid)
            elif event == conf.NET_CONNECTION_NEW:
                print "No implemented !!!!!!!!"
        except:
            print "Handle received message error !!!!!!!!"


def main():
    host = ""
    port = 34567

    server = Server(host, port)
    while True:
        server.tick()
        time.sleep(0.001)


if __name__ == '__main__':
    main()
