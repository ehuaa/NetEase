using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class EnemyHealth : MonoBehaviour {
    public int startingHealth = 100;
    public int currentHealth;
    public float sinkSpeed = 2.5f;
    public int scoreValue = 10;
    public AudioClip deathClip;

    Animator anim;
    AudioSource enemyAudio;
    ParticleSystem hitParticles;
    CapsuleCollider capsuleCollider;
    bool isDead;
    bool isSinking;

    void Awake()
    {
        anim = GetComponent<Animator>();
        enemyAudio = GetComponent<AudioSource>();
        hitParticles = GetComponentInChildren<ParticleSystem>();
        capsuleCollider = GetComponent<CapsuleCollider>();

        currentHealth = startingHealth;
    }

    void Update()
    {
        if (isSinking)
        {
            transform.Translate(-Vector3.up * sinkSpeed * Time.deltaTime);
        }
    }
    
    public void TakeMagicDamage(int amount)
    {
        if (isDead)
            return;

        enemyAudio.Play();

        //currentHealth -= amount;
               
        hitParticles.transform.localPosition = new Vector3(0f, 2.0f, 0f);

        var render = hitParticles.GetComponent<Renderer>();
        Material mat = render.material;
        mat.color = new Color(0.0f, 0.2f, 0.8f);
        render.material = mat;
        
        hitParticles.Play();

        if (currentHealth <= 0)
        {
            Death();
        }
    }

    public void TakeDamage(int amount, Vector3 hitPoint)
    {
        if (isDead)
            return;

        enemyAudio.Play();

        //currentHealth -= amount;
        hitParticles.transform.position = hitPoint;

        var render = hitParticles.GetComponent<Renderer>();
        Material mat = render.material;
        mat.color = new Color(0.8f, 0.2f, 0.0f);
        render.material = mat;

        hitParticles.Play();

        if (currentHealth <= 0)
        {
            Death();
        }
    }

    public void Death()
    {
        isDead = true;

        currentHealth = 0;

        capsuleCollider.isTrigger = true;

        anim.SetTrigger("Dead");

        enemyAudio.clip = deathClip;
        enemyAudio.Play();
    }

    public void StartSinking()
    {
        GetComponent<NavMeshAgent>().enabled = false;

        GetComponent<Rigidbody>().isKinematic = true;

        isSinking = true;

        ScoreManager.score+=scoreValue;

        Destroy(gameObject, 2f);
    }
}
