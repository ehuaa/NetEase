using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class LoginManager : MonoBehaviour {

    public InputField userName;
    public InputField passWord;
    NetworkSocket networkSocket;
    GameObject networkManager;

    void Awake()
    {
        networkManager = GameObject.FindGameObjectWithTag("NetworkManager");
        networkSocket = this.networkManager.GetComponent<NetworkSocket>();
    }
        
    //Go to the mainscene
    void ChangeScene()
    {
        SceneManager.LoadScene("mainscene");        
    }

    //Login helper for test.
    public void TestLogin(string username)
    {
        login(username, "163"/*test account password*/);
    }

    //Login function will be called outside.
    public void LoginCall()
    {
        login(userName.text, passWord.text);        
    }

    //Login function : The real login action
    void login(string username, string password)
    {      
        if (username =="" || password == "")
        {
            Debug.Log("username or password is empty");
            return;
        }

        MsgCSLogin msg = new MsgCSLogin(username, password);

        byte[] data = msg.GetRawData();

        this.networkSocket.writeSocket(data);
        
        return;
    }
}
