using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OtherPlayerController : MonoBehaviour {
    
    public float speed = 3f;            

    Vector3 movement;     
    Animator anim;        
    Rigidbody playerRigidbody;
    
    public int userID = -1;
    public int entityID = -1;

    void Awake ()
    {
        anim = GetComponent <Animator> ();
                        
        playerRigidbody = GetComponent <Rigidbody> ();
    }

    void LateUpdate()
    {
        anim.SetBool ("IsWalking", false);
    }
    
    public void MoveTo (Vector3 movement)
    {        
        playerRigidbody.MovePosition (transform.position + movement);
        anim.SetBool("IsWalking", true);
    }        
}
