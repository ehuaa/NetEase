using System.Collections;
using System.Collections.Generic;

public class MsgCSBase{
    public int msgCommond = -1;
    
    public virtual byte[] GetMessageData()
    {
        return null;
    }
}
