using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MsgCSReplay:MsgCSBase{
    
    public MsgCSReplay(int userID)
    {
        this.msgCommond = command.MSG_CS_GAME_REPLAY;
        this.userID = userID;
    }    
}
