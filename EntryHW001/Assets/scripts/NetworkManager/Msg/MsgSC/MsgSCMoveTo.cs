using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class MsgSCMoveTo{

    int userID;
    int entityID;
    Vector3 movement;
    
    public MsgSCMoveTo(BinaryReader br)
    {
        try
        {
            this.userID = br.ReadInt32();
            this.entityID = br.ReadInt32();
            this.movement.x = br.ReadSingle();
            this.movement.y = br.ReadSingle();
            this.movement.z = br.ReadSingle();
        }
        catch
        {
            Debug.Log("MsgSCConfirm err");
        }        
    }

    public int EntityID()
    {
        return this.entityID;
    }

    public int GetUserID()
    {
        return this.userID;
    }

    public Vector3 GetMovement()
    {
        return this.movement;
    }
}