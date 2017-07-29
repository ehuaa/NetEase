using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class MsgSCMoney {
    public int userID;
    public int money;
    
    public MsgSCMoney(BinaryReader br)
    {
        try
        {
            this.userID = br.ReadInt32();
            this.money = br.ReadInt32();
        }
        catch
        {
            Debug.Log("MsgSCPlayerAttack err");
        }        
    }
}
