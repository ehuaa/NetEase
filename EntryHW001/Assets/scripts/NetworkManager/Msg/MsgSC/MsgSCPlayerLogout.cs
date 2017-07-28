using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class MsgSCPlayerLogout {

    public int userID;
    public int entityID;

    public MsgSCPlayerLogout(BinaryReader br)
    {
        try
        {
            userID = br.ReadInt32();
            entityID = br.ReadInt32();
        }
        catch
        {
            Debug.Log("MsgSCPlayerLogout Err");
        }
    }
}
