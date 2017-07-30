using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PlayerHealth : MonoBehaviour {
    public int startingHealth = 100;
    public int currentHealth;        
    public AudioClip deathClip;
    public float flashSpeed = 5f;
    public Color flashColor = new Color(1.0f, 0.0f, 0.0f, 0.1f);
    Button birth;

    Animator anim;
    Image damageImage;
    AudioSource playerAudio;
    PlayerController playerMovement;
    PlayerShooting playerShooting;
    Slider healthSlider;
    bool damaged;

    void Awake()
    {
        anim = GetComponent<Animator>();
        playerAudio = GetComponent<AudioSource>();
        playerMovement = GetComponent<PlayerController>();
        playerShooting = GetComponentInChildren<PlayerShooting>();
        healthSlider = GameObject.Find("HealthSlider").GetComponent<Slider>();
        damageImage = GameObject.Find("DamageImage").GetComponent<Image>();
        birth = GameObject.Find("Birth").GetComponent<Button>();
        currentHealth = startingHealth;
        healthSlider.value = currentHealth;
        birth.gameObject.SetActive(false);
    }

    void Update()
    {
        if (damaged)
           damageImage.color = flashColor;
        else
           damageImage.color = Color.Lerp(damageImage.color, Color.clear, flashSpeed * Time.deltaTime);

        damaged = false;
    }

    public void TakeDamage(int amount)
    {
        damaged = true;        
        healthSlider.value = currentHealth;
        playerAudio.Play();
    }

    public void SetBloodValue(int Blood)
    {
        currentHealth = Blood;
        healthSlider.value = currentHealth;
    }

    public void Death()
    {        
        playerShooting.DisableEffects();

        anim.SetTrigger("Die");
        playerAudio.clip = deathClip;
        playerAudio.Play();
        playerMovement.enabled = false;
        playerShooting.enabled = false;

        birth.gameObject.SetActive(true);
    }    
}
