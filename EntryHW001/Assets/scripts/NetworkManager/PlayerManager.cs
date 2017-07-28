using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerManager : MonoBehaviour {

    public GameObject player;
    public GameObject otherplayer;

    public Dictionary<int, GameObject> playerArray = new Dictionary<int, GameObject>();

    public void DeleteOtherPlayer(MsgSCPlayerLogout msg)
    {
        GameObject obj = playerArray[msg.userID];
        playerArray.Remove(msg.userID);

        Destroy(obj);
    }
    
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

            if (msg.GetUserID() == opc.GetComponent<EntityAttributes>().ID)
            {
                opc.MoveTo(msg.GetMovement());
            }
        }
    }
    
	public GameObject CreatePlayer(int userID, int entityID, Vector3 pos,Quaternion quat, bool actor)
    {
        GameObject obj = null;
        EntityAttributes ea = null;
        //Other players
        if (actor != true)
        {


            obj = Instantiate(otherplayer, pos, quat);
            
            ea = obj.GetComponent<EntityAttributes>();

            ea.ID = userID;
            ea.ID = entityID;
            playerArray.Add(ea.ID, obj);
            
            return obj;
        }

        // Current player
        obj = Instantiate(player, pos, quat);
       
        ea = obj.GetComponent<EntityAttributes>();
        ea.ID = userID;
        ea.EntityID = entityID;

        CameraFollower cam = Camera.main.GetComponent<CameraFollower>();
        
        if (cam != null)
        {
            cam.SetCameraPosition(obj.transform.position);
            cam.target = obj.transform;
            cam.SetOffset();
        }

        playerArray.Add(ea.ID, obj);
        return obj;
    }
    
    public void OtherPlayerAttack(MsgSCPlayerAttack msg)
    {
        GameObject obj = playerArray[msg.userID];
        OtherPlayerShooting ops = obj.GetComponentInChildren<OtherPlayerShooting>();

        if (msg.kind == MsgSCPlayerAttack.WEAPON_ATTACK)
        {
            ops.ShootArrow();
        }
        else if(msg.kind == MsgSCPlayerAttack.MAGIC_ATTACK)
        {
            ops.ShootMagic();
        }
    }
}
