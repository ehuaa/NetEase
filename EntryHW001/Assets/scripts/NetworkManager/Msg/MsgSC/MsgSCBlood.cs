using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class MsgSCBlood{

    public int userID;
    public int blood; 
    
    public MsgSCBlood(BinaryReader br)
    {
        try
        {
            this.userID = br.ReadInt32();
            this.blood = br.ReadInt32();
        }
        catch
        {
            Debug.Log("MsgSCBlood err");
        }        
    }
}
