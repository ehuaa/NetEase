using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrapTest : MonoBehaviour {
    public GameObject trap;

    public void CreateTrap()
    {
        GameObject obj = Instantiate(trap);

        TrapController tc = obj.GetComponent<TrapController>();

        tc.onAir = true;
    }
}
