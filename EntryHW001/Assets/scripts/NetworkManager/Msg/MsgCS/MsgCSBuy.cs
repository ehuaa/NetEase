using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MsgCSBuy:MsgCSBase{

    int trapID;

    public MsgCSBuy(int trapID)
    {
        this.msgCommond = command.MSG_CS_BUY;
        this.trapID = trapID;
    }

    public override void DataGenerate()
    {
        bw.Write(this.trapID);
    }
}
