using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraFollower : MonoBehaviour {
    public Transform target;
    public float smoothing = 5f;

    Vector3 offset;

    void Start()
    {
        if (target == null)
            return;

        offset = transform.position - target.position;
    }

    public void SetOffset()
    {
        offset = transform.position - target.position;
    }

    void FixedUpdate()
    {
        if (target == null)
            return;

        Vector3 targetCampos = target.position + offset;

        transform.position = Vector3.Lerp(transform.position, targetCampos, smoothing * Time.deltaTime);
    }
}
