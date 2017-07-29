using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class EnemyMovement : MonoBehaviour {
        
    bool bmove = false;
    Vector3 localmove;
    float speed;

    void Awake()
    {
        speed = 300;
    }

    void FixedUpdate()
    {
        if (bmove == true && gameObject.transform.position != localmove)
        {
            float delta = Time.deltaTime / (speed / 1000);
            speed = speed - Time.deltaTime*1000;

            gameObject.transform.position = Vector3.Lerp(gameObject.transform.position, localmove, delta);            
        }
    }

    public void MoveTo(Vector3 pos, float speed)
    {
        bmove = true;
        localmove = pos;
        this.speed = speed;
    }
}
