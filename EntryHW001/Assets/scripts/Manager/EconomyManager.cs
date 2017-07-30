using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class EconomyManager : MonoBehaviour {

    public Canvas storeCanvas;        

    void Awake()
    {
        storeCanvas.gameObject.SetActive(false);
    }
    
    public void ShowStorePanel()
    {
        storeCanvas.gameObject.SetActive(true);
    }

    public void BuyTrapOne()
    {
        MsgCSBuy msg = new MsgCSBuy(1);
        var center = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<NetworkMsgSendCenter>();
        center.SendMessage(msg);
    }
    
    public void BuyTrapTwo()
    {
        MsgCSBuy msg = new MsgCSBuy(2);
        var center = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<NetworkMsgSendCenter>();
        center.SendMessage(msg);
    }

    public void Close()
    {
        storeCanvas.gameObject.SetActive(false);
    }
}
