using System.Collections;
using System.Collections.Generic;
using System;
using System.IO;

using UnityEngine;

public class NetworkMsgSendCenter : MonoBehaviour {
    
    NetworkSocket socket;
    GameSceneManager gamescenemanager;    

    void Awake()
    {
        socket = GetComponent<NetworkSocket>();
        gamescenemanager = GetComponent<GameSceneManager>();
    }
    
    void Update()
    {
        MsgDispatch();
    }

    void MsgDispatch()
    {
        byte[] data = socket.readSocket();

        if (data == null)
            return;

        BinaryReader br= this.GetBinaryReader(data);

        int code = br.ReadInt32();

        switch (code)
        {
            case command.MSG_SC_CONFIRM:
                this.MsgSCConfirmProcedure(br);
                break;
            case command.MSG_SC_SCENE_LOAD:
                this.MsgSCLoadsceneProcedure(br);
                break;
            case command.MSG_SC_MOVETO:
                this.MsgSCMoveToProcedure(br);
                break;
            default:
                Debug.Log("defualt sc message !!");
                break;
        }
    }

    BinaryReader GetBinaryReader(byte[] data)
    {
        MemoryStream sm = new MemoryStream(data);
        return new BinaryReader(sm);
    }

    void MsgSCConfirmProcedure(BinaryReader br)
    {
         MsgSCConfirm msg = new MsgSCConfirm(br);
        if (msg.GetMessage() == MsgSCConfirm.MSG_OK)
        {
            gamescenemanager.userID = msg.GetUserID();
            gamescenemanager.ChangeScene();          
        }
        else
        {
            Debug.Log("SC msg err !");
        }
    }

    void MsgSCLoadsceneProcedure(BinaryReader br)
    {
        MsgSCLoadscene msg = new MsgSCLoadscene(br);
        gamescenemanager.CreateEntity(msg);
    }

    void MsgSCMoveToProcedure(BinaryReader br)
    {
        MsgSCMoveTo msg = new MsgSCMoveTo(br);
        gamescenemanager.MoveToMessage(msg);
    }

    public void SendMessage(MsgCSBase msg)
    {
        byte[] data = msg.GetMessageData();
        socket.writeSocket(data);
    }
}
