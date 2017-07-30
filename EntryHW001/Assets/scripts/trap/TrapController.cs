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
        EnemyManager em = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<EnemyManager>();
        if (em.IsEnemyGameObject(other.gameObject) == true)
        {
            other.gameObject.GetComponent<EnemyHealth>().Hurt();
            int id1 = gameObject.GetComponent<EntityAttributes>().EntityID;
            int id2 = other.gameObject.GetComponent<EntityAttributes>().EntityID;

            MsgCSTrapAttack msg = new MsgCSTrapAttack(id1, id2);
            NetworkMsgSendCenter center = GameObject.FindGameObjectWithTag("NetworkManager").GetComponent<NetworkMsgSendCenter>();
            center.SendMessage(msg);
        }
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
