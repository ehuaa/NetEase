# -*- coding: GBK -*-

MSG_SC_CONFIRM = 0x1001
MSG_SC_MOVETO = 0x1002
MSG_SC_ENEMY_BORN = 0x1003
MSG_SC_ENEMY_DIE = 0x1004
MSG_SC_PLAYER_BLOOD = 0x1005
MSG_SC_ENEMY_BLOOD = 0x1006
MSG_SC_TIMER = 0x1007 # Reset timer for the next wave of enemies
MSF_SC_ENEMY_DONE = 0x1008 # Enemy arrive the destination
MSG_SC_PLAYER_UPGRADE = 0x1009
MSG_SC_MONEY=0x100a # Update money value
MSG_SC_SCENE_LOAD=0x100b # Load entities
MSG_SC_BACKPACK=0x100c #Update backpack value
MSG_SC_SPEED = 0x100d #Update player's speed
MSG_SC_DISTANCE = 0x100e #Update player's shoot distance
MSG_SC_TRAP_DIE = 0x100f
MSG_SC_PLAYER_DIE = 0x1010
MSG_SC_PLAYER_ATTACK = 0x1011
MSG_SC_PLAYER_LOGOUT = 0x1012
MSG_SC_GAME_WIN = 0x1013
MSG_SC_GAME_OVER = 0x1014

MSG_CS_LOGIN = 0x2001
MSG_CS_LOGOUT = 0x2002
MSG_CS_MOVETO = 0x2003
MSG_CS_ATTACK = 0x2004
MSG_CS_ENEMY_ATTACK = 0x2005
MSG_CS_WEAPON_UPGRADE = 0x2006
MSG_CS_MONEY = 0x2007 #Buy weapon
MSG_CS_WEAPON_ATTACK = 0x2008
MSG_CS_GAME_REPLAY = 0x2009
MSG_CS_TRAP_IN = 0x200a
MSG_CS_BUY = 0x200b
MSG_CS_TRAP_ATTACK = 0x200c

MSG_SS_GAME_OVER = 0x3001

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
