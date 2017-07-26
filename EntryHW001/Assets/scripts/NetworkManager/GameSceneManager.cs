using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameSceneManager : MonoBehaviour {

    EnemySpawn enemyspawn;
    TrapManager trapmanager;
    PlayerManager playermanager;

    public int userID = -12;

    void Awake()
    {
        enemyspawn = GetComponent<EnemySpawn>();
        playermanager = GetComponent<PlayerManager>();
        trapmanager = GetComponent<TrapManager>();
    }


    public void ChangeScene()
    {
        SceneManager.LoadScene("mainscene");
    }

    public void MoveToMessage(MsgSCMoveTo msg)
    {
        if (msg.GetUserID() != -1)
        {
            if (msg.GetUserID() == this.userID)
            {
                playermanager.MovePlayer(msg);
            }
            else
            {
                playermanager.MoveOPlayer(msg);
            }
        }
        else
        {
            //EnemyMove
        }
    }

    public void CreateEntity(MsgSCLoadscene msg)
    {
        GameObject obj = null;

        
        if (msg.GetKind() == MsgSCLoadscene.MSG_KIND_ENEMY)
            obj = enemyspawn.Spawn(msg.GetID(), msg.GetEntityID(), msg.GetPosition(), msg.GetQuat());

        if (msg.GetKind() == MsgSCLoadscene.MSG_KIND_TRAP)
            obj = trapmanager.CreateTrap(msg.GetID(), msg.GetEntityID(), msg.GetPosition(), msg.GetQuat());

        if (msg.GetKind() == MsgSCLoadscene.MSG_KIND_PLAYER)
        {
            if (msg.GetID() == this.userID)
                obj = playermanager.CreatePlayer(msg.GetID(), msg.GetEntityID(),msg.GetPosition(), msg.GetQuat(), true);
            else
                obj = playermanager.CreatePlayer(msg.GetID(), msg.GetEntityID() ,msg.GetPosition(), msg.GetQuat(), false);
        }        
    }
}
