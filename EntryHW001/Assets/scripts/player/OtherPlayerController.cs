using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OtherPlayerController : MonoBehaviour {
    
    public float speed = 3f;            

    Vector3 movement;     
    Animator anim;        
    Rigidbody playerRigidbody;
    
    public int userID = -1;

    void Awake ()
    {
        anim = GetComponent <Animator> ();
                        
        playerRigidbody = GetComponent <Rigidbody> ();
    }
    
    void Move (float h, float v)
    {
        movement.Set (h, 0f, v);
        
        movement = movement.normalized * speed * Time.deltaTime;

        playerRigidbody.MovePosition (transform.position + movement);
    }
        
    void Animating (float h, float v)
    {
        bool walking = h != 0f || v != 0f;
        
        anim.SetBool ("IsWalking", walking);
    }
}
