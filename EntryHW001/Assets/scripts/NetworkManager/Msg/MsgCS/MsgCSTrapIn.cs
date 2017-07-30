using UnityEngine;

public class MsgCSTrapIn : MsgCSBase{
    Vector3 pos;
    int trapID;

    public MsgCSTrapIn(Vector3 pos, int trapID)
    {
        this.msgCommond = command.MSG_CS_TRAP_IN;
        this.pos = pos;
        this.trapID = trapID;
    }

    public override void DataGenerate()
    {
        bw.Write(this.trapID);
        bw.Write(pos.x);
        bw.Write(pos.y);
        bw.Write(pos.z);     
    }
}
