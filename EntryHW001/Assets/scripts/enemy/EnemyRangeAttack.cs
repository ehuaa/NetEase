using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyRangeAttack : MonoBehaviour {

    public float timeBwteenAttacks = 1.0f;
    public int attackDamage = 0;
    public float range = 500.0f;
    public float attackRange = 20.0f;
    public Transform firepoint;

    int shootableMask;

    GameObject player;
    PlayerHealth playerHealth;    

    Ray shootRay=new Ray();
    RaycastHit shootHit;
    
    float timer;
    LineRenderer gunLine;
    EnemyHealth enemyHealth;

    float effectsDisplayTime = 0.2f;

    void Awake()
    {
        shootableMask = LayerMask.GetMask("PlayerLayer");

        player = GameObject.FindGameObjectWithTag("Player");
        playerHealth = player.GetComponent<PlayerHealth>();
        gunLine = GetComponent<LineRenderer>();
        enemyHealth = GetComponent<EnemyHealth>();
    }
       
    void FixedUpdate()
    {
        timer += Time.deltaTime;
        Attack();

        if(timer>=timeBwteenAttacks * effectsDisplayTime)
        {
            gunLine.enabled = false;
        }
    }

    void Attack()
    {
        if (timer < timeBwteenAttacks || playerHealth.currentHealth < 0 || enemyHealth.currentHealth < 0)
            return;

        Vector3 posPlayer = player.transform.position;
        Vector3 posCurrent = this.firepoint.position;

        posPlayer.y = posCurrent.y;

        Vector3 vec = posPlayer - posCurrent;

        if (vec.magnitude < attackRange)
        {
            shootRay.origin = this.firepoint.position;
            vec.Normalize();

            shootRay.direction = vec;          

            if (Physics.Raycast(shootRay, out shootHit, range, shootableMask))
            {
                PlayerHealth playerHealth = shootHit.collider.GetComponent<PlayerHealth>();
                if (playerHealth != null)
                {
                    playerHealth.TakeDamage(attackDamage);

                    timer = 0;

                    gunLine.enabled = true;
                    gunLine.SetPosition(0, shootRay.origin);
                    gunLine.SetPosition(1, posPlayer);
                }                
            }
        }
    }
}
