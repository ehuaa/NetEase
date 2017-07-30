using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrapController : MonoBehaviour {
    float camRayLength;    
    int floorMask;
    public bool onAir;
    public int trapID = -1;

    void Awake()
    {
        camRayLength = 500;
        floorMask = LayerMask.GetMask("floor");
        onAir = false;
    }

    void OnTriggerEnter(Collider other)
    {
        Debug.Log("One Hit");
    }

    void Update()
    {
        if (onAir == true)
        {
            GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<PlayerManager>().DisablePlayerShooting();
            
            Vector3 pos;
            if (this.GetFloorPosition(out pos)== true)
            {
                this.transform.position = pos;
            }
            
            if (Input.GetMouseButtonDown(0) == true)
            {
                this.onAir = false;
                
                //Send Message To Server
                gameObject.SetActive(false);
                Destroy(gameObject);               
                GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<PlayerManager>().EnablePlayerShooting();

                MsgCSTrapIn msg = new MsgCSTrapIn(this.transform.position, this.trapID);
                NetworkMsgSendCenter center = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<NetworkMsgSendCenter>();
                center.SendMessage(msg);
                                
            }
            else if (Input.GetMouseButtonDown(1) == true)
            {
                gameObject.SetActive(false);
                Destroy(gameObject);

                GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<PlayerManager>().EnablePlayerShooting();
            }
        }
    }
    
    bool GetFloorPosition(out Vector3 pos)
    {
        Ray camRay = Camera.main.ScreenPointToRay (Input.mousePosition);

        RaycastHit floorHit;
        
        if(Physics.Raycast (camRay, out floorHit, camRayLength, floorMask))
        {
            pos = floorHit.point;
            return true;
        }
        pos = new Vector3();
        return false;
    }
}
