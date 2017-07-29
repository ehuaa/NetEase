using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrapController : MonoBehaviour {
    float camRayLength;    
    int floorMask;
    public bool onAir;

    void Awake()
    {
        camRayLength = 500;
        floorMask = LayerMask.GetMask("floor");
        onAir = false;
    }

    void Update()
    {
        if (onAir == true)
        {
            Vector3 pos;
            if (this.GetFloorPosition(out pos)== true)
            {
                this.transform.position = pos;
            }
            
            if (Input.GetMouseButtonDown(0) == true)
            {
                this.onAir = false;
                pos = this.transform.position;
                pos.y = 0.55f;
                this.transform.position = pos;
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
