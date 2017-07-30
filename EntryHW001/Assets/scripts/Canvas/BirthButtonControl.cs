using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class BirthButtonControl : MonoBehaviour {

    public Button birth;

    void Awake()
    {        
    }        
	
	// Update is called once per frame
	void Update () {
		
	}

    public void Birth()
    {
        PlayerManager pm = GameObject.Find("NetworkManager").GetComponent<PlayerManager>();
        pm.DestroyPlayer();
        birth.gameObject.SetActive(false);

        GameObject obj = GameObject.Find("NetworkManager");
        GameSceneManager gsm = obj.GetComponent<GameSceneManager>();
        gsm.ReplayGame();
        SceneManager.LoadScene("mainscene");
    }
}
