# -*- coding: GBK -*-

import time

from Services.UserServices import UserServices
from common import conf
from common import events
from common.dispatcher import Dispatcher
from common.header import Header
from network.simpleHost import SimpleHost
from Database.DBManager import DBManager
from Managers.RoomManager import RoomManager

class Server(object):
    def __init__(self, host, port):
        super(Server, self).__init__()

        # Start host
        self.host = SimpleHost()
        self.host.startup(host, port)

        self.host.db_manager = DBManager(conf.DB_NAME)
        self.host.room_manager = RoomManager(self.host)

        self.user_services = UserServices(self.host)

        # rooms
        self.rooms = []

        # Generate dispatcher
        self.dispatcher = Dispatcher()
        self.register_dispatcher_services()

        # map msg_type to message object
        self.msg_dict = None
        self.generate_msg_dict()

    def register_dispatcher_services(self):
        self.dispatcher.register(conf.USER_SERVICES, self.user_services)
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
        # ***************************************************
        # Not implemented let the RoomManager tick()
        # ****************************************************


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
                    if client_hid in self.user_services.client_hid_to_user_map:
                        self.host.room_manager.handle_received_msg(msg_type, data, client_hid)
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
    port = 2000

    server = Server(host, port)
    while True:
        server.tick()
        #time.sleep(0.001)


if __name__ == '__main__':
    main()
