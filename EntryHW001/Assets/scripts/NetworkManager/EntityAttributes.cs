using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class EntityAttributes : MonoBehaviour {
    public int ID = -1;
    public int EntityID = -1;
    public int Blood = -1;
    public int Money = -1;
    public int Speed = -1;

    public int trapOne = 0;    
    public int trapTwo = 0;

    public void SetBackpack(MsgSCBackpack msg)
    {
        this.trapOne = msg.num1;
        this.trapTwo = msg.num2;


        GameObject.Find("Canvas/TrapOne").GetComponentInChildren<Text>().text = "TrapOne:" + msg.num1.ToString();
        GameObject.Find("Canvas/TrapTwo").GetComponentInChildren<Text>().text = "TrapTwo:" + msg.num2.ToString();
    }
}
