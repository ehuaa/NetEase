using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class EnemyMovement : MonoBehaviour {
    Transform target;
    PlayerHealth playerHealth;
    EnemyHealth enemyHealth;
    NavMeshAgent nav;
    
    public int EnemyID;
    public int EntityID;

    void Awake()
    {
        target = GameObject.FindGameObjectWithTag("target").transform;

        enemyHealth = GetComponent<EnemyHealth>();

        nav = GetComponent<NavMeshAgent>();
    }

    void Update()
    {
        if (enemyHealth.currentHealth > 0)
        {
            nav.SetDestination(target.position);
        }
        else
        {
            nav.enabled = false;
        }
    }
}
