using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class MsgCSMove : MsgCSBase
{
    Vector3 pos;
    int userID;
    public MsgCSMove(Vector3 pos, int userID)
    {
        this.msgCommond = command.MSG_CS_MOVETO;
        this.pos = pos;
        this.userID = userID;
    }

    public override byte[] GetMessageData()
    {
        MemoryStream sm = new MemoryStream();
        BinaryWriter bw = new BinaryWriter(sm);
        
        bw.Write(this.msgCommond);
        bw.Write(this.userID);
        bw.Write(pos.x);
        bw.Write(pos.y);
        bw.Write(pos.z);

        byte[] data = sm.GetBuffer();
        byte[] buf = new byte[sm.Length];

        Array.Copy(data, 0, buf, 0, sm.Length);

        return buf;        
    }
}
