using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class MsgSCPlayerDie{
    public int userID;
    public MsgSCPlayerDie(BinaryReader br)
    {
        this.userID = br.ReadInt32();
    }
}
