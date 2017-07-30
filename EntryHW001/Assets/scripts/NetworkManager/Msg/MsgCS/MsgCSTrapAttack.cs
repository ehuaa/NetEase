using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MsgCSTrapAttack:MsgCSBase{

    int id1;
    int id2;

    public MsgCSTrapAttack(int entityID1, int entityID2)
    {
        this.msgCommond = command.MSG_CS_TRAP_ATTACK;
        id1 = entityID1;
        id2 = entityID2;
    }

    public override void DataGenerate()
    {
        bw.Write(id1);
        bw.Write(id2);
    }
}
