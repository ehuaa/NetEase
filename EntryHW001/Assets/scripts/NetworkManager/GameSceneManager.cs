using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameSceneManager : MonoBehaviour {

    EnemyManager enemymanager;
    TrapManager trapmanager;
    PlayerManager playermanager;

    public int userID = -12;

    public int GetUserID()
    {
        return userID;
    }

    void Awake()
    {
        enemymanager = GetComponent<EnemyManager>();
        playermanager = GetComponent<PlayerManager>();
        trapmanager = GetComponent<TrapManager>();
    }

    public void OtherPlayerAttack(MsgSCPlayerAttack msg)
    {
        playermanager.OtherPlayerAttack(msg);
    }

    public void DestoryEnemy(MsgSCEnemyDie msg)
    {
        enemymanager.DestroyEnemy(msg.entityID);
    }

    public void DestroyOtherPlayer(MsgSCPlayerLogout msg)
    {
        playermanager.DeleteOtherPlayer(msg);
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
            enemymanager.MoveEnemyToPosition(msg);
        }
    }

    public void CreateEntity(MsgSCLoadscene msg)
    {        
        if (msg.GetKind() == MsgSCLoadscene.MSG_KIND_ENEMY)
            enemymanager.Spawn(msg.GetID(), msg.GetEntityID(), msg.GetPosition(), msg.GetQuat());

        if (msg.GetKind() == MsgSCLoadscene.MSG_KIND_TRAP)
            trapmanager.CreateTrap(msg.GetID(), msg.GetEntityID(), msg.GetPosition(), msg.GetQuat());

        if (msg.GetKind() == MsgSCLoadscene.MSG_KIND_PLAYER)
        {
            if (msg.GetID() == this.userID)
                playermanager.CreatePlayer(msg.GetID(), msg.GetEntityID(),msg.GetPosition(), msg.GetQuat(), true);
            else
                playermanager.CreatePlayer(msg.GetID(), msg.GetEntityID() ,msg.GetPosition(), msg.GetQuat(), false);
        }        
    }
}
