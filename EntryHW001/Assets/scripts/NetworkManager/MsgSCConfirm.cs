using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class MsgSCConfirm{
    public const int MSG_ERR_PROG = 1;
    public const int MSG_ERR_PW = 2;
    public const int MSG_OK = 0;
    public const int MSG_ERR_UNKNOWN = 3;

    int msg = MSG_ERR_UNKNOWN;
    int userID = -1;
    
    public MsgSCConfirm(BinaryReader br)
    {
        try
        {
            this.userID = br.ReadInt32();
            this.msg = br.ReadInt32();
        }
        catch
        {
            Debug.Log("MsgSCConfirm err");
        }        
    }

    public int GetMessage()
    {
        return this.msg;
    }

    public int GetUserID()
    {
        return this.userID;
    }
}
