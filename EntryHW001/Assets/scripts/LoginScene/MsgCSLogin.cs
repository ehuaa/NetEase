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

    public void WriteSocket(NetworkSocket socket)
    {
        BinaryWriter bw = socket.GetWriteSocket();

        if (bw == null)
        {
            Debug.Log("server not right");
            return;
        }
        
        int header = 0;
        int commandcode = command.MSG_CS_LOGIN;
        byte[] name = System.Text.Encoding.Default.GetBytes(userName);
        byte[] pw = System.Text.Encoding.Default.GetBytes(password);
        int nlen = name.Length;
        int plen = pw.Length;

        header = 16 + nlen + plen;

        bw.Write(header);
        bw.Write(commandcode);
        bw.Write(nlen);
        bw.Write(name);
        bw.Write(plen);
        bw.Write(pw);

        bw.Flush();
    }
}
