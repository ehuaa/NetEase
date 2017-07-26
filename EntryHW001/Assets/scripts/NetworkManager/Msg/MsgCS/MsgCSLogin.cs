using System;
using System.IO;
using UnityEngine;

public class MsgCSLogin
{
    string userName;
    string password;

    public MsgCSLogin(string name, string pw)
    {
        this.userName = name;
        this.password = pw;
    }

    public byte[] GetRawData()
    {
        MemoryStream sm = new MemoryStream();
        BinaryWriter bw = new BinaryWriter(sm);
        
        int commandcode = command.MSG_CS_LOGIN;
        byte[] name = System.Text.Encoding.Default.GetBytes(userName);
        byte[] pw = System.Text.Encoding.Default.GetBytes(password);
        int nlen = name.Length;
        int plen = pw.Length;
        
        bw.Write(commandcode);
        bw.Write(nlen);
        bw.Write(name);
        bw.Write(plen);
        bw.Write(pw);

        byte[] data = sm.GetBuffer();
        byte[] buf = new byte[sm.Length];

        Array.Copy(data, 0, buf, 0, sm.Length);

        return buf;        
    }
}
