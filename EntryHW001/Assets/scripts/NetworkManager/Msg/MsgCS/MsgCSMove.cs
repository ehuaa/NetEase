using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class MsgCSMove : MsgCSBase
{
    Vector3 pos;

    public MsgCSMove(Vector3 pos, int userID)
    {
        this.msgCommond = command.MSG_CS_MOVETO;
        this.pos = pos;
        this.userID = userID;
    }

    public override void DataGenerate()
    {                
        bw.Write(pos.x);
        bw.Write(pos.y);
        bw.Write(pos.z);     
    }
}
