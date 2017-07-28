using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyManager : MonoBehaviour {

    public GameObject EnemyBear;
    public GameObject EnemyBunny;

    public Dictionary<int, GameObject> enemyArray = new Dictionary<int, GameObject>();

    public void MoveEnemyToPosition(MsgSCMoveTo msg)
    {
        EnemyMovement em = enemyArray[msg.EntityID()].GetComponent<EnemyMovement>();
        em.MoveTo(msg.GetMovement(), msg.speed);
    }

    public GameObject Spawn(int ID, int EntityID, Vector3 pos, Quaternion quat)
    {
        GameObject obj = null;
        if (ID == 1)
        {
            obj = Instantiate(EnemyBear, pos, quat);
        }
        else
        {
            obj = Instantiate(EnemyBunny, pos, quat);
        }

        EntityAttributes ea = obj.GetComponent<EntityAttributes>();
        ea.ID = ID;
        ea.EntityID = EntityID;

        this.enemyArray.Add(EntityID, obj);

        return obj;
    }
    
    public void DestroyEnemy(int entityID)
    {
        GameObject obj = this.enemyArray[entityID];
        enemyArray.Remove(entityID);

        EnemyHealth health = obj.GetComponent<EnemyHealth>();
        health.Death();
    }
}
