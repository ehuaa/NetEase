using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class MsgSCBackpack{

    public int trapID1;
    public int trapID2;

    public int num1;
    public int num2;

	public MsgSCBackpack(BinaryReader br)
    {
        this.trapID1 = br.ReadInt32();
        this.num1 = br.ReadInt32();
        this.trapID2 = br.ReadInt32();
        this.num2 = br.ReadInt32();        
    }
}
