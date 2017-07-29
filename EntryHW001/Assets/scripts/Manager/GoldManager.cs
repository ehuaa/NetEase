using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GoldManager : MonoBehaviour {
    
    public static int gold;

    Text text;

    void Awake()
    {
        text = GetComponent<Text>();
        gold = 0;
    }

    void Update()
    {
        text.text = "Gold: " + gold;
    }
}
