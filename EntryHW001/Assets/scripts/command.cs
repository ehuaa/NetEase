﻿using System;

public class command
{
    public static int MSG_SC_CONFIRM = 0x1001;
    public static int MSG_SC_MOVETO = 0x1002;
    public static int MSG_SC_ENEMY_BORN = 0x1003;
    public static int MSG_SC_ENEMY_DIE = 0x1004;
    public static int MSF_SC_ENEMY_DONE = 0x1008;
    public static int MSG_SC_ACTOR_BLOOD = 0x1005;
    public static int MSG_SC_ENEMY_BLOOD = 0x1006;
    public static int MSG_SC_TIMER = 0x1007; // Reset timer for the next wave of enemies
    public static int MSG_SC_ACTOR_UPGRADE = 0x1009;
    public static int MSG_SC_MONEY = 0x100a; // Update money value

    public static int MSG_CS_LOGIN = 0x1001;
    public static int MSG_CS_MOVETO = 0x2002;
    public static int MSG_CS_ACTOR_ATTACK = 0x2003;
    public static int MSG_CS_ENEMY_ATTACK = 0x2004;
    public static int MSG_CS_WEAPON_UPGRADE = 0x2005;
    public static int MSG_CS_MONEY = 0x2006; //Buy weapon
    public static int MSG_CS_WEAPON_ATTACK = 0x2007;


    public static int NET_STATE_STOP = 0;// state: init value
    public static int NET_STATE_CONNECTING = 1;        // state: connecting
    public static int NET_STATE_ESTABLISHED = 2;   // state: connected

    public static int NET_HEAD_LENGTH_SIZE = 4;// 4 bytes little endian (x86)
    public static string NET_HEAD_LENGTH_FORMAT = "<I";

    public static int NET_CONNECTION_NEW = 0;// new connection
    public static int NET_CONNECTION_LEAVE = 1; // lost connection
    public static int NET_CONNECTION_DATA = 2;// data come

    public static int NET_HOST_DEFAULT_TIMEOUT = 70;

    public static int MAX_HOST_CLIENTS_INDEX = 0xffff;
    public static int MAX_HOST_CLIENTS_BYTES = 16;
}
