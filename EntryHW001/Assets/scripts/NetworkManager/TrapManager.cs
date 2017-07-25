using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrapManager : MonoBehaviour {

	public GameObject trapPin;
    public GameObject trapSpeed;

    public void CreateTrap(int ID, int EntityID, Vector3 pos, Quaternion quat)
    {
        GameObject obj = null;
        if (ID == 1)
        {
            obj = Instantiate(trapPin, pos, quat);
        }
        else
        {
            obj = Instantiate(trapSpeed, pos, quat);
        }
      
        TrapController tc = obj.GetComponent<TrapController>();
        tc.TrapID = ID;
        tc.EntityID = EntityID;
    }
}
