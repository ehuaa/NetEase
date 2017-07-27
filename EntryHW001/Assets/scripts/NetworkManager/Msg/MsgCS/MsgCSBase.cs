using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class MsgCSBase{
    public int msgCommond = -1;
    public int userID = -1;

    protected MemoryStream sm;
    protected BinaryWriter bw;

    public MsgCSBase()
    {
        sm = new MemoryStream();
        bw = new BinaryWriter(sm);
    }

    public virtual void DataGenerate()
    {
        return;
    }

    public byte[] GetMessageData()        
    {
        CmdUserIDGenerate();
        DataGenerate();
        
        byte[] data = sm.GetBuffer();
        byte[] buf = new byte[sm.Length];

        Array.Copy(data, 0, buf, 0, sm.Length);

        return buf;
    }
    
    public void CmdUserIDGenerate()
    {
        GameSceneManager sm = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<GameSceneManager>();
        this.userID = sm.GetUserID();

        this.bw.Write(this.msgCommond);
        this.bw.Write(this.userID);
    }

    public void Vector3Generate(Vector3 pos)
    {
        bw.Write(pos.x);
        bw.Write(pos.y);
        bw.Write(pos.z);     
    }
}
