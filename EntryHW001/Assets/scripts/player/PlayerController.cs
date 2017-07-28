using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour {


    public float speed = 3f;            

    Vector3 movement;     
    Animator anim;        
    Rigidbody playerRigidbody;
    int floorMask;            
    float camRayLength = 500f;

    NetworkMsgSendCenter msgcenter;
    Vector3 moveSum;

    Vector3 localMove;

    bool bmove = false;    

    void Awake ()
    {
        floorMask = LayerMask.GetMask ("floor");
                
        anim = GetComponent <Animator> ();
                        
        playerRigidbody = GetComponent <Rigidbody> ();

        msgcenter = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<NetworkMsgSendCenter>();

        moveSum = new Vector3(0, 0, 0);
    }

    void FixedUpdate ()
    {
        float h = Input.GetAxisRaw ("Horizontal");
        float v = Input.GetAxisRaw ("Vertical");

        Move (h, v);
                
        Animating(h, v);

        if (bmove == true && gameObject.transform.position != localMove)
        {
            gameObject.transform.position = Vector3.Lerp(gameObject.transform.position, localMove, 0.2f);            
        }
    }

    void Move (float h, float v)
    {
        movement.Set (h, 0f, v);
        
        movement = movement.normalized * speed * Time.deltaTime;        
        
        if (h !=0 || v!= 0)
        {
            Animating(h, v);
            moveSum = moveSum + movement;

            if (moveSum.magnitude > 0.5)
            {
                MsgCSMove msg = new MsgCSMove(moveSum, this.GetComponent<EntityAttributes>().ID);
                msgcenter.SendMessage(msg);
                moveSum = new Vector3(0, 0, 0);
            }
        }            
    }

    public void MoveTo(Vector3 move)
    {        
        bmove = true;
        localMove = move;
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
