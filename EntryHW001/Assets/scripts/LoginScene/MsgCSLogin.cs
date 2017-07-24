using System;
using System.IO;

public class MsgCSLogin
{
    string userName;
    string password;

    public MsgCSLogin(string name, string pw)
    {
        this.userName = name;
        this.password = pw;
    }

    public void WriteSocket(BinaryWriter net_writer)
    {       
    }
}
