using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameSceneManager : MonoBehaviour {

    EnemyManager enemymanager;
    TrapManager trapmanager;
    PlayerManager playermanager;
    NetworkMsgSendCenter msgcenter;

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
        msgcenter = GetComponent<NetworkMsgSendCenter>();
    }

    public void PlayerDie(MsgSCPlayerDie msg)
    {
        if (msg.userID == this.userID)
            playermanager.PlayerDie(msg);
        else
            playermanager.OtherPlayerDie(msg);
    }

    public void SetPlayerBoold(MsgSCBlood msg)
    {
        playermanager.SetPlayerBlood(msg);
    }

    public void GameWin(MsgSCGameWin msg)
    {
        playermanager.InitPlayerManager();
        enemymanager.InitEnemyManager();
        GameWinManager gwm = GameObject.FindGameObjectWithTag("Canvas").GetComponent<GameWinManager>();
        gwm.GameWin();
    }

    public void ReplayGame()
    {
        MsgCSReplay msg = new MsgCSReplay(this.userID);
        msgcenter.SendMessage(msg);
        playermanager.InitPlayerManager();
        enemymanager.InitEnemyManager();
    }
    
    public void GameOver(MsgSCGameOver msg)
    {
        GameOverManager govm = GameObject.FindGameObjectWithTag("Canvas").GetComponent<GameOverManager>();
        playermanager.DestroyPlayer();
        govm.GameOver();
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

        if (msg.GetEntityID() == MsgSCLoadscene.MSG_KIND_TRAP)
        {
            trapmanager.CreateTrap(msg.GetID(), msg.GetEntityID(), msg.GetPosition(), msg.GetQuat());
        }
    }
    
    public void SetBackpack(MsgSCBackpack msg)
    {
        playermanager.SetBackpack(msg);
    }
}
