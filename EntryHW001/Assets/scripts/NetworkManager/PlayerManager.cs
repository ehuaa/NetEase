using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;


public class PlayerManager : MonoBehaviour {

    public GameObject player;
    public GameObject otherplayer;

    public Dictionary<int, GameObject> playerArray = new Dictionary<int, GameObject>();

    public void DisablePlayerShooting()
    {
        GameSceneManager gsm = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<GameSceneManager>();

        if (playerArray.ContainsKey(gsm.userID) == false)
            return;

        PlayerShooting ps = playerArray[gsm.userID].GetComponentInChildren<PlayerShooting>();
        ps.enabled = false;
    }
    
    public void EnablePlayerShooting()
    {
        GameSceneManager gsm = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<GameSceneManager>();

        PlayerShooting ps = playerArray[gsm.userID].GetComponentInChildren<PlayerShooting>();
        ps.enabled = true;
    }

    public void SetBackpack(MsgSCBackpack msg)
    {
        GameSceneManager gs = GetComponent<GameSceneManager>();

        GameObject obj = GetPlayerOjb(gs.userID);
        
        if (obj != null)
        {
            EntityAttributes ea = obj.GetComponent<EntityAttributes>();
            ea.SetBackpack(msg);
        }                
    }   

    public GameObject GetPlayerOjb(int userID)
    {
        if (playerArray.ContainsKey(userID) == true)
            return playerArray[userID];

        return null;
    }

    public void PlayerDie(MsgSCPlayerDie msg)
    {
        GameObject obj = this.playerArray[msg.userID];
        PlayerHealth ph = obj.GetComponent<PlayerHealth>();
        ph.Death();
    }

    public void OtherPlayerDie(MsgSCPlayerDie msg)
    {
        if (playerArray.ContainsKey(msg.userID) == false)
            return;

        GameObject obj = this.playerArray[msg.userID];
        OtherPlayerController opc = obj.GetComponent<OtherPlayerController>();
        opc.Death();
    }

    public void SetPlayerBlood(MsgSCBlood msg)
    {
        PlayerHealth ph = playerArray[msg.userID].GetComponent<PlayerHealth>();
        ph.SetBloodValue(msg.blood);
    }

    public void DestroyPlayer()
    {
        GameSceneManager gsm = GetComponent<GameSceneManager>();
        GameObject obj = playerArray[gsm.userID];
        obj.SetActive(false);        
        playerArray.Remove(gsm.userID);
        Destroy(obj);
    }

    public void DeleteOtherPlayer(MsgSCPlayerLogout msg)
    {
        if (playerArray.ContainsKey(msg.userID) == false)
            return;

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

            if (playerArray.ContainsKey(ea.ID) == true)
            {
                Destroy(playerArray[ea.ID]);
                playerArray.Remove(ea.ID);
            }
           
                        
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
    
    public void InitPlayerManager()
    {
        foreach(KeyValuePair<int, GameObject> cell in this.playerArray)
        {
            cell.Value.SetActive(false);
            Destroy(cell.Value);
        }
        playerArray.Clear();
    }
}
