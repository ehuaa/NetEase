using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerShooting : MonoBehaviour {
    public int damagePerShot = 20;
    public int magicPerShot = 5;

    public float timeBetweenBullets = 0.2f;
    public float timeBetweenMagic = 5.0f;
    public float range = 500f;
    public Material[] materials;

    float timerBullets;
    float timerMagic;

    float effecttime;

    Ray shootRay=new Ray();
    RaycastHit shootHit;

    int shootableMask;
    ParticleSystem gunParticles;
    LineRenderer gunLine;
    AudioSource gunAudio;
    Light gunLight;

    float effectsDisplayTime = 0.2f;
    
    void Awake()
    {
        shootableMask = LayerMask.GetMask("shootable");

        gunParticles = GetComponent<ParticleSystem>();
        gunLine = GetComponent<LineRenderer>();
        gunAudio = GetComponent<AudioSource>();
        gunLight = GetComponent<Light>();
    }

    void Update()
    {
        timerBullets += Time.deltaTime;
        timerMagic += Time.deltaTime;
        effecttime += Time.deltaTime;

        if (Input.GetButton("Fire1") && timerBullets >= timeBetweenBullets)
        {
            ShootArrow();
        }

        if (Input.GetButton("Fire2") && timerMagic>= this.timeBetweenMagic)
        {
            ShootMagic();
        }

        if(effecttime >= timeBetweenBullets * effectsDisplayTime)
        {
            DisableEffects();
        }
    }

    public void DisableEffects()
    {
        gunLine.enabled = false;
        gunLight.enabled = false;
    }

    void ShootArrow()
    {
        timerBullets = 0f;
        effecttime = 0f;

        gunAudio.Play();
       
        gunLight.color = new Color(0.9f, 0.9f, 0.0f);
        gunLight.enabled = true;

        gunParticles.Stop();
        gunParticles.Play();

        gunLine.material = this.materials[0];

        gunLine.enabled = true;
        gunLine.SetPosition(0, transform.position);


        shootRay.origin = transform.position;
        shootRay.direction = transform.forward;

        if (Physics.Raycast(shootRay, out shootHit, range, shootableMask))
        {           
            EnemyHealth enemyHealth = shootHit.collider.GetComponent<EnemyHealth>();
            if (enemyHealth != null)
            {                
                enemyHealth.TakeDamage(damagePerShot, shootHit.point);

                MsgCSAttack msg = new MsgCSAttack(this.GetComponentInParent<EntityAttributes>().EntityID, shootHit.collider.GetComponent<EntityAttributes>().EntityID, shootRay.origin, shootHit.point, MsgCSAttack.WEAPON_ATTACK);
                
                NetworkMsgSendCenter msgcenter = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<NetworkMsgSendCenter>();
                msgcenter.SendMessage(msg);
            }
            else
            {
                MsgCSAttack msg = new MsgCSAttack(this.GetComponentInParent<EntityAttributes>().EntityID, -1, new Vector3(0,0,0), new Vector3(0,0,0), MsgCSAttack.WEAPON_ATTACK);
                
                NetworkMsgSendCenter msgcenter = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<NetworkMsgSendCenter>();
                msgcenter.SendMessage(msg);
            }

            gunLine.SetPosition(1, shootHit.point);
        }
        else
        {                        
            gunLine.SetPosition(1, shootRay.origin + shootRay.direction * range);

            MsgCSAttack msg = new MsgCSAttack(this.GetComponentInParent<EntityAttributes>().EntityID, -1, new Vector3(0,0,0), new Vector3(0,0,0), MsgCSAttack.WEAPON_ATTACK);

            NetworkMsgSendCenter msgcenter = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<NetworkMsgSendCenter>();
            msgcenter.SendMessage(msg);
        }
    }
    
    void ShootMagic()
    {
        timerMagic = 0f;
        effecttime = 0f;

        gunAudio.Play();
        gunLight.enabled = true;
        gunLight.color = new Color(0.1f, 0.3f, 1.0f);

        gunParticles.Stop();
        gunParticles.Play();

        gunLine.material = this.materials[1];
                        
        gunLine.enabled = true;
        gunLine.SetPosition(0, transform.position);

        shootRay.origin = transform.position;
        shootRay.direction = transform.forward;

        if (Physics.Raycast(shootRay, out shootHit, range, shootableMask))
        {
            float radius = 3.0f;
            Collider[] colliders = Physics.OverlapSphere(shootHit.point, radius);

            foreach(Collider cld in colliders)
            {
                EnemyHealth enemyHealth = cld.GetComponent<EnemyHealth>();
                if (enemyHealth != null)
                {
                    enemyHealth.TakeMagicDamage(this.magicPerShot);                   
                }                
            }

            if (colliders.Length > 0)
            {
                MsgCSAttack msg = new MsgCSAttack(this.GetComponentInParent<EntityAttributes>().EntityID, shootHit.collider.GetComponent<EntityAttributes>().EntityID, shootRay.origin, shootHit.point, MsgCSAttack.MAGIC_ATTACK);

                NetworkMsgSendCenter msgcenter = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<NetworkMsgSendCenter>();
                msgcenter.SendMessage(msg);
            }
            else
            {
                MsgCSAttack msg = new MsgCSAttack(this.GetComponentInParent<EntityAttributes>().EntityID, -1, new Vector3(0, 0, 0), new Vector3(0, 0, 0), MsgCSAttack.MAGIC_ATTACK);

                NetworkMsgSendCenter msgcenter = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<NetworkMsgSendCenter>();
                msgcenter.SendMessage(msg);
            }

            gunLine.SetPosition(1, shootHit.point);
        }
        else
        {            
            gunLine.SetPosition(1, shootRay.origin + shootRay.direction * range);

            MsgCSAttack msg = new MsgCSAttack(this.GetComponentInParent<EntityAttributes>().EntityID, -1, new Vector3(0,0,0), new Vector3(0,0,0), MsgCSAttack.MAGIC_ATTACK);

            NetworkMsgSendCenter msgcenter = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<NetworkMsgSendCenter>();
            msgcenter.SendMessage(msg);
        }
    }
}
