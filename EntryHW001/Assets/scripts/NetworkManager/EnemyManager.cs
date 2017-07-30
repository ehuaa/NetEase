using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyManager : MonoBehaviour {

    public GameObject EnemyBear;
    public GameObject EnemyBunny;

    public Dictionary<int, GameObject> enemyArray = new Dictionary<int, GameObject>();

    public bool IsEnemyGameObject(GameObject obj)
    {
        EntityAttributes ea = obj.GetComponent<EntityAttributes>();
        if (ea == null)
            return false;

        if (enemyArray.ContainsKey(ea.EntityID) == false)
            return false;

        return true;
    }

    public void MoveEnemyToPosition(MsgSCMoveTo msg)
    {
        if (enemyArray.ContainsKey(msg.EntityID()) == false)
            return;

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

        if (enemyArray.ContainsKey(ea.EntityID) == true)
        {
            enemyArray[ea.EntityID].SetActive(false);
            Destroy(enemyArray[ea.EntityID]);
            enemyArray.Remove(ea.EntityID);
        }

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

    public void InitEnemyManager()
    {
        foreach(KeyValuePair<int, GameObject> cell in this.enemyArray)
        {
            cell.Value.SetActive(false);
            Destroy(cell.Value);
        }
        enemyArray.Clear();
    }
}
