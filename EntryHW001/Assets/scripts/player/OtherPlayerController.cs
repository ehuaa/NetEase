using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OtherPlayerController : MonoBehaviour {    
    public AudioClip deathClip;

    Vector3 movement;     
    AudioSource playerAudio;
    Animator anim;        
    Vector3 localmove;
    bool bmove = false;
    
    
    void Awake ()
    {
        anim = GetComponent <Animator> ();                        
        playerAudio = GetComponent<AudioSource>();
    }

    void Update()
    {
        if (bmove == true && gameObject.transform.position != localmove)
        {
            anim.SetBool("IsWalking", true);
            gameObject.transform.position = Vector3.Lerp(gameObject.transform.position, localmove, 0.2f);
        }
    }

    void LateUpdate()
    {
        anim.SetBool ("IsWalking", false);
    }
    
    public void MoveTo (Vector3 movement)
    {
        bmove = true;
        localmove = movement;        
    }   

    public void Death()
    {
        anim.SetTrigger("Die");
        playerAudio.clip = deathClip;
        playerAudio.Play();
        Debug.Log("Die");
    }
}
