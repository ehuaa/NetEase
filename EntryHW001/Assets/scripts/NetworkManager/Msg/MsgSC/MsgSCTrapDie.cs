using System.IO;

public class MsgSCTrapDie {

    public int entityID;
    public MsgSCTrapDie(BinaryReader br)
    {
        entityID = br.ReadInt32();
    }
}
