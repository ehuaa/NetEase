using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameSceneManager : MonoBehaviour {

    EnemySpawn enemyspawn;
    PlayerManager playermanager;

    public int userID = -1;

    void Awake()
    {
        enemyspawn = GetComponent<EnemySpawn>();
        playermanager = GetComponent<PlayerManager>();
    }


    public void ChangeScene()
    {
        SceneManager.LoadScene("mainscene");
    }

    public void CreateEntity(MsgSCLoadscene msg)
    {
        if (msg.GetEntityID() != -1)
        {
            enemyspawn.Spawn(msg.GetID(), msg.GetEntityID(), msg.GetPosition(), msg.GetQuat());
            
            return;
        }   

        if (msg.GetID() == this.userID)
        {
            playermanager.CreatePlayer(msg.GetID(), msg.GetPosition(), msg.GetQuat(), true);
        }
        else
        {
            playermanager.CreatePlayer(msg.GetID(), msg.GetPosition(), msg.GetQuat(), false);
        }
    }
}
