using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class MsgSCEnemyDie
{        
    public int entityID;
        
    public MsgSCEnemyDie(BinaryReader br)
    {
        try
        {
            this.entityID = br.ReadInt32();
        }
        catch
        {
            Debug.Log("MsgSCEnemyDie err");
        }        
    }    
}
