from Entity.Room import Room


class RoomManager(object):
    def __init__(self, host):
        self.host = host
        self.rid_to_game_room_map = {}
        self.waiting_room = Room(self.generate_room_id(), self.host)
        self.username_to_room_map = {}
        self.client_hid_to_user={}

    def handle_received_msg(self, msg_type, data, client_hid):
        if self.client_hid_to_user.has_key(client_hid) is False:
            return

        # find room and send msg
        room = self.username_to_room_map[self.client_hid_to_user[client_hid].username]
        room.handle_received_msg(msg_type,data,client_hid)

    def generate_room_id(self):
        for id in xrange(1,len(self.rid_to_game_room_map)+2):
            if self.rid_to_game_room_map.has_key(id) is False:
                return id

    def tick(self):
        for room in self.rid_to_game_room_map.itervalues():
            if room.is_valid() is False:
                self._remove_room(room)
            else:
                room.tick()

    def add_user(self, user):

        # join the room again
        if self.username_to_room_map.has_key(user.username) is True:
            room = self.username_to_room_map.has_key(user.username)
            room.add_user(user)
            return

        # new user is coming
        if self.waiting_room.add_user(user) is False:
            self.rid_to_game_room_map[self.waiting_room.rid] = self.waiting_room
            self.waiting_room = Room(self.generate_room_id(), self.host)
            self.waiting_room.add_user(user)

        self.username_to_room_map[user.username] = self.waiting_room
        self.client_hid_to_user[user.client_hid] = user

    def remove_user(self, user):
        if self.username_to_room_map.has_key(user.username) is False:
            return

        room = self.username_to_room_map[user.username]

        if room.remove_user(user) is True:
            # The room is empty
            del self.rid_to_game_room_map[room.rid]
            for k,v in room.username_to_user_map.items():
                del self.username_to_room_map[k]

    # remove invalid room
    def _remove_room(self, room):
        del self.rid_to_game_room_map[room.rid]

        for user in room.username_to_user_map.itervalues():
            del self.username_to_room_map[user.username]
            del self.client_hid_to_user[user.client_hid]
