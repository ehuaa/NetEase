﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour {


    public float speed = 3f;            

    Vector3 movement;     
    Animator anim;        
    Rigidbody playerRigidbody;
    int floorMask;            
    float camRayLength = 500f;

    public int userID = -1;

    void Awake ()
    {
        floorMask = LayerMask.GetMask ("floor");
                
        anim = GetComponent <Animator> ();
                        
        playerRigidbody = GetComponent <Rigidbody> ();
    }

    void FixedUpdate ()
    {
        float h = Input.GetAxisRaw ("Horizontal");
        float v = Input.GetAxisRaw ("Vertical");

        Move (h, v);
        Animating (h, v);

        Turning ();        
    }

    void Move (float h, float v)
    {
        movement.Set (h, 0f, v);
        
        movement = movement.normalized * speed * Time.deltaTime;

        playerRigidbody.MovePosition (transform.position + movement);
    }

    void Turning ()
    {        
        Ray camRay = Camera.main.ScreenPointToRay (Input.mousePosition);

        RaycastHit floorHit;
        
        if(Physics.Raycast (camRay, out floorHit, camRayLength, floorMask))
        {
            Vector3 playerToMouse = floorHit.point - transform.position;

            playerToMouse.y = 0f;
            
            Quaternion newRotation = Quaternion.LookRotation (playerToMouse);

            playerRigidbody.MoveRotation (newRotation);
        }        
    }

    void Animating (float h, float v)
    {
        bool walking = h != 0f || v != 0f;
        
        anim.SetBool ("IsWalking", walking);
    }
}
