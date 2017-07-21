# -*- coding: GBK -*-

MSG_CS_LOGIN = 0x1001
MSG_SC_CONFIRM = 0x2001

MSG_CS_MOVETO = 0x1002
MSG_SC_MOVETO = 0x2002

NET_STATE_STOP = 0				# state: init value
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
