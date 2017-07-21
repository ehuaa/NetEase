using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkMsgSendCenter : MonoBehaviour {

	public class MsgCMD
    {
        public static int LOGIN = 0x0001;
        public static int MOVE = 0x0002;
    }

    NetworkSocket socket;

    void Awake()
    {
        socket = GetComponent<NetworkSocket>();
    }
    
    public void Login(string username, string password)
    {        
    }
}
