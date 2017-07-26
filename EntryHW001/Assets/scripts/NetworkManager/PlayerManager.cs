using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerManager : MonoBehaviour {

    public GameObject player;
    public GameObject otherplayer;
    
    public void MovePlayer(MsgSCMoveTo msg)
    {
        GameObject obj = GameObject.FindGameObjectWithTag("Player");
        PlayerController pc = obj.GetComponent<PlayerController>();
        pc.MoveTo(msg.GetMovement());
    }
    
    public void MoveOPlayer(MsgSCMoveTo msg)
    {
        GameObject[] obj = GameObject.FindGameObjectsWithTag("otherPlayer");

        for (int k = 0; k < obj.Length; k++)
        {
            OtherPlayerController opc = obj[k].GetComponent<OtherPlayerController>();

            if (msg.GetUserID() == opc.userID)
            {
                opc.MoveTo(msg.GetMovement());
            }
        }
    }
    
	public GameObject CreatePlayer(int userID, int entityID, Vector3 pos,Quaternion quat, bool actor)
    {
        GameObject obj = null;
        //Other players
        if (actor != true)
        {
            obj = Instantiate(otherplayer, pos, quat);
            OtherPlayerController opc = obj.GetComponent<OtherPlayerController>();

            opc.userID = userID;
            opc.entityID = entityID;
            
            return obj;
        }

        // Current player
        obj = Instantiate(player, pos, quat);
       
        PlayerController pc = obj.GetComponent<PlayerController>();
        pc.userID = userID;
        pc.entityID = entityID;

        CameraFollower cam = Camera.main.GetComponent<CameraFollower>();
        
        if (cam != null)
        {
            cam.target = obj.transform;
            cam.SetOffset();
        }


        return obj;
    }
}
