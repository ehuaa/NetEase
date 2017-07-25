using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerManager : MonoBehaviour {

    public GameObject player;
    public GameObject otherplayer;
    
	public void CreatePlayer(int userID, Vector3 pos,Quaternion quat, bool actor)
    {
        //Other players
        if (actor != true)
        {
            return;
        }

        // Current player
        GameObject obj = Instantiate(player, pos, quat);
       
        PlayerController pc = obj.GetComponent<PlayerController>();
        pc.userID = userID;
        CameraFollower cam = Camera.main.GetComponent<CameraFollower>();
        
        if (cam != null)
        {
            cam.target = obj.transform;
            cam.SetOffset();
        }


        return;
    }
}
