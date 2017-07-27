using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OtherPlayerShooting : MonoBehaviour {

    public float timeBetweenBullets = 0.15f;
    public float range = 500f;

    public Material[] materials;

    float timer;

    Ray shootRay=new Ray();
    RaycastHit shootHit;

    int shootableMask;
    ParticleSystem gunParticles;
    LineRenderer gunLine;
    AudioSource gunAudio;
    Light gunLight;

    float effectsDisplayTime = 0.1f;
    
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
        timer += Time.deltaTime;
                
        if(timer>=timeBetweenBullets * effectsDisplayTime)
        {
            DisableEffects();
        }
    }

    public void DisableEffects()
    {
        gunLine.enabled = false;
        gunLight.enabled = false;
    }

    public void ShootArrow()
    {
        timer = 0f;
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
                enemyHealth.TakeDamage(0, shootHit.point);                
            }

            gunLine.SetPosition(1, shootHit.point);
        }
        else
        {            
            gunLine.SetPosition(1, shootRay.origin + shootRay.direction * range);
        }
    }
    
    public void ShootMagic()
    {
        timer = 0f;
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
                    enemyHealth.TakeMagicDamage(0);
                }
            }

            gunLine.SetPosition(1, shootHit.point);
        }
        else
        {            
            gunLine.SetPosition(1, shootRay.origin + shootRay.direction * range);
        }
    }
}
