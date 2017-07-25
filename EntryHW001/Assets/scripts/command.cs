using System;

public class command
{
    public const int MSG_SC_CONFIRM = 0x1001;
    public const int MSG_SC_MOVETO = 0x1002;
    public const int MSG_SC_ENEMY_BORN = 0x1003;
    public const int MSG_SC_ENEMY_DIE = 0x1004;
    public const int MSG_SC_ACTOR_BLOOD = 0x1005;
    public const int MSG_SC_ENEMY_BLOOD = 0x1006;
    public const int MSG_SC_TIMER = 0x1007; // Reset timer for the next wave of enemies
    public const int MSF_SC_ENEMY_DONE = 0x1008; // Enemy arrive the destination
    public const int MSG_SC_ACTOR_UPGRADE = 0x1009;
    public const int MSG_SC_MONEY = 0x100a; // Update money value
    public const int MSG_SC_SCENE_LOAD = 0x100b; // Load entities

    public const int MSG_CS_LOGIN = 0x2001;
    public const int MSG_CS_LOGOUT = 0x2002;
    public const int MSG_CS_MOVETO = 0x2003;
    public const int MSG_CS_ACTOR_ATTACK = 0x2004;
    public const int MSG_CS_ENEMY_ATTACK = 0x2005;
    public const int MSG_CS_WEAPON_UPGRADE = 0x2006;
    public const int MSG_CS_MONEY = 0x2007; //Buy weapon
    public const int MSG_CS_WEAPON_ATTACK = 0x2008;


    public const int NET_STATE_STOP = 0;           // state: init value
    public const int NET_STATE_CONNECTING = 1;     // state: connecting
    public const int NET_STATE_ESTABLISHED = 2;        // state: connected

    public const int NET_HEAD_LENGTH_SIZE = 4;     // 4 bytes little endian (x86)
    public const string NET_HEAD_LENGTH_FORMAT = "<I";

    public const int NET_CONNECTION_NEW = 0;       // new connection
    public const int NET_CONNECTION_LEAVE = 1;    // lost connection
    public const int NET_CONNECTION_DATA = 2;      // data come

    public const int NET_HOST_DEFAULT_TIMEOUT = 70;

    public const int MAX_HOST_CLIENTS_INDEX = 0xffff;
    public const int MAX_HOST_CLIENTS_BYTES = 16;
}
