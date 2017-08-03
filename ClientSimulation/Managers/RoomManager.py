from Entity.Room import Room

class RoomManager(object):
    def __init__(self, host):
        self.host = host
        self.rid_to_game_room_map = {}
        self.waiting_room = Room(self.generate_room_id(), self.host)
        self.username_to_room_map = {}

    def handle_received_msg(self, msg_type, data, client_hid):
        pass

    def generate_room_id(self):
        for id in xrange(1,len(self.rid_to_game_room_map)+2):
            if self.rid_to_game_room_map.has_key(id) == False:
                return id

    def add_user(self, user):
        try:
            # join the room again
            if self.username_to_room_map.has_key(user.username) == True:
                room = self.username_to_room_map.has_key(user.username)
                room.add_user(user)
                return

            # New user is coming
            if self.waiting_room.add_user(user) == False:
                self.rid_to_game_room_map[self.waiting_room.rid] = self.waiting_room
                # When the room is full start game
                self.waiting_room.start_game()
                self.waiting_room = Room(self.generate_room_id(), self.host)
            else:
                self.waiting_room.add_user(user)

            self.username_to_room_map[user.username] = self.waiting_room
        except:
            print "RoomManager add_user error"

    def remove_user(self, user):
        if self.username_to_room_map.has_key(user.username) == False:
            return

        room = self.username_to_room_map[user.username]

        if room.remove_user(user) == True:
            # The room is empty
            del self.rid_to_game_room_map[room.rid]
            for k,v in room.username_to_user_map.items():
                del self.username_to_room_map[k]
        else:
            # Remove nothing.
            pass
