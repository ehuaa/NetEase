using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class MsgSCLoadscene
{
    public const int intMSG_KIND_PLAYER = 0;
    public const int MSG_KIND_ENEMY = 1;
    public const int MSG_KIND_TRAP = 2;

    Vector3 position;
    Quaternion quat;
    int kind;
    int ID;
    int EntityID;
    
    public MsgSCLoadscene(BinaryReader br)
    {
        try
        {
            kind = br.ReadInt32();
            ID = br.ReadInt32();
            EntityID = br.ReadInt32();
            position.x = br.ReadSingle();
            position.y = br.ReadSingle();
            position.z = br.ReadSingle();
            quat.w = br.ReadSingle();
            quat.x = br.ReadSingle();
            quat.y = br.ReadSingle();
            quat.z = br.ReadSingle();
        }
        catch
        {
            Debug.Log("MsgSCLoadscene Err");
        }
    }

    public int GetKind()
    {
        return kind;
    }

    public int GetID()
    {
        return this.ID;
    }

    public int GetEntityID()
    {
        return this.EntityID;
    }
    
    public Vector3 GetPosition()
    {
        return position;
    }

    public Quaternion GetQuat()
    {
        return this.quat;
    }
}
