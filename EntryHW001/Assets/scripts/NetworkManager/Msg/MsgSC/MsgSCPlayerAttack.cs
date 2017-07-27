using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class MsgSCPlayerAttack{
    
    public const int WEAPON_ATTACK = 0;
    public const int MAGIC_ATTACK = 1;

    public int userID;
    public int entityID;
    public int kind;

    
    public MsgSCPlayerAttack(BinaryReader br)
    {
        try
        {
            this.userID = br.ReadInt32();
            this.entityID = br.ReadInt32();
            this.kind = br.ReadInt32();
        }
        catch
        {
            Debug.Log("MsgSCPlayerAttack err");
        }        
    }
}
