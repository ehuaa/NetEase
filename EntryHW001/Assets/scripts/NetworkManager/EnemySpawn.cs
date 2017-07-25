using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemySpawn : MonoBehaviour {

    public GameObject EnemyBear;
    public GameObject EnemyBunny;

    public void Spawn(int ID, int EntityID, Vector3 pos, Quaternion quat)
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
        
        EnemyMovement move = obj.GetComponent<EnemyMovement>();
        move.EnemyID = ID;
        move.EntityID = EntityID;
    }
}
