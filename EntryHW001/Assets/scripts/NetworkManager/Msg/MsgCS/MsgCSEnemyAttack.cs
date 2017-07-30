using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MsgCSEnemyAttack : MsgCSBase {
        
    int entityID1;
    int entityID2;

    public MsgCSEnemyAttack(int entityIDAttacker, int entityIDVictim)
    {
        this.msgCommond = command.MSG_CS_ENEMY_ATTACK;

        this.entityID1 = entityIDAttacker;
        this.entityID2 = entityIDVictim;        
    }
    public override void DataGenerate()
    {        
        this.bw.Write(this.entityID1);
        this.bw.Write(this.entityID2);
    }
}
