using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrapManager : MonoBehaviour {

	public GameObject trapPin;
    public GameObject trapSpeed;

    Dictionary<int, GameObject> trapArray = new Dictionary<int, GameObject>();

    public void DestroyTrap(int entityID)
    {
        if (trapArray.ContainsKey(entityID) == false)
            return;

        GameObject obj = trapArray[entityID];
        trapArray.Remove(entityID);

        obj.SetActive(false);
        Destroy(obj);
    }
    
    public GameObject CreateTrap(int ID, int EntityID, Vector3 pos, Quaternion quat)
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
      
        EntityAttributes ea = obj.GetComponent<EntityAttributes>();
        ea.ID = ID;
        ea.EntityID = EntityID;

        addTrapArray(ea.EntityID, obj);

        return obj;
    }

    void addTrapArray(int entityID, GameObject obj)
    {
        if (this.trapArray.ContainsKey(entityID) == true)
        {
            trapArray[entityID].SetActive(false);
            Destroy(trapArray[entityID]);
            trapArray.Remove(entityID);
        }

        trapArray.Add(entityID, obj);
    }
    
    public void CreateTrapPin()
    {
        GameObject obj = Instantiate(this.trapPin, this.trapPin.transform.position, this.trapPin.transform.rotation);
        TrapController tc = obj.GetComponent<TrapController>();

        tc.onAir = true;
        tc.trapID = 1;
    }

    public void CreateTrapSpeed()
    {
        GameObject obj = Instantiate(this.trapSpeed, this.trapPin.transform.position, this.trapPin.transform.rotation);
        TrapController tc = obj.GetComponent<TrapController>();

        tc.onAir = true;
        tc.trapID = 2;
    }
}
