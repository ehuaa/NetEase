using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MsgCSAttack : MsgCSBase {

    public const int WEAPON_ATTACK = 0;
    public const int MAGIC_ATTACK = 1;
    public const int ENEMY_NEAR = 2;
    public const int ENEMY_FAR = 3;
    public const int TRAP_BOOLD = 4;
    public const int TRAP_SPEED = 5;
    
    int entityID1;
    int entityID2;
    Vector3 pos1;
    Vector3 pos2;
    int attack_kind;

    public MsgCSAttack(int entityIDAttacker, int entityIDVictim, Vector3 pos1, Vector3 pos2, int kind)
    {
        this.msgCommond = command.MSG_CS_ATTACK;

        this.entityID1 = entityIDAttacker;
        this.entityID2 = entityIDVictim;

        this.pos1 = pos1;
        this.pos2 = pos2;

        this.attack_kind = kind;
    }
    public override void DataGenerate()
    {        
        this.bw.Write(this.entityID1);
        this.bw.Write(this.entityID2);
        this.Vector3Generate(pos1);
        this.Vector3Generate(pos2);
        this.bw.Write(this.attack_kind);        
    }
}
