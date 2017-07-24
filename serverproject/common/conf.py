# -*- coding: GBK -*-


MSG_SC_CONFIRM = 0x1001
MSG_SC_MOVETO = 0x1002
MSG_SC_ENEMY_BORN = 0x1003
MSG_SC_ENEMY_DIE = 0x1004
MSG_SC_ACTOR_BLOOD = 0x1005
MSG_SC_ENEMY_BLOOD = 0x1006
MSG_SC_TIMER = 0x1007 # Reset timer for the next wave of enemies
MSF_SC_ENEMY_DONE = 0x1008 # Enemy arrive the destination
MSG_SC_ACTOR_UPGRADE = 0x1009
MSG_SC_MONEY=0x100a # Update money value

MSG_CS_LOGIN = 0x2001
MSG_CS_LOGOUT = 0x2002
MSG_CS_MOVETO = 0x2003
MSG_CS_ACTOR_ATTACK = 0x2004
MSG_CS_ENEMY_ATTACK = 0x2005
MSG_CS_WEAPON_UPGRADE = 0x2006
MSG_CS_MONEY = 0x2007 #Buy weapon
MSG_CS_WEAPON_ATTACK = 0x2008


NET_STATE_STOP = 0			# state: init value
NET_STATE_CONNECTING = 1		# state: connecting
NET_STATE_ESTABLISHED = 2		# state: connected

NET_HEAD_LENGTH_SIZE = 4		# 4 bytes little endian (x86)
NET_HEAD_LENGTH_FORMAT = '<I'

NET_CONNECTION_NEW = 0	    # new connection
NET_CONNECTION_LEAVE = 1    # lost connection
NET_CONNECTION_DATA = 2	    # data come

NET_HOST_DEFAULT_TIMEOUT = 70

MAX_HOST_CLIENTS_INDEX = 0xffff
MAX_HOST_CLIENTS_BYTES = 16
