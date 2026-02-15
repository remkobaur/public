using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectRain : MonoBehaviour
{
    public GameObject prefab = null;
    public float frequency = 10f;
    public float angularRate = 10f;
    public float angle = 10f;
    public float thrust = 300f;
    public int maxAmout = 50;

    public bool enableRandomColor = true;

    private float startTime =0f;
    private List<GameObject> buffer = new List<GameObject>();
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        rainObjects();
    }

    private void rainObjects()
    {
        if (Time.time > startTime && frequency>0)
        {
            startTime = Time.time+1f/frequency;

            spawnObject(Vector3.zero);
        }
    }

    private void spawnObject(Vector3 _pos)
    {
        GameObject go = Instantiate(prefab, new Vector3(0, 0, 0), Quaternion.identity);
        go.transform.parent =transform;
        go.transform.position = transform.position+_pos;

        if (enableRandomColor)
        {
            go.GetComponent<Renderer>().material.color = UnityEngine.Random.ColorHSV() ;
        }
        Vector3 direction = Quaternion.Euler(angle,angularRate*10*Time.time,0f)*Vector3.up;
        go.GetComponent<Rigidbody>().AddForce(direction * thrust);

        buffer.Add(go);
        while (buffer.Count>maxAmout)
        {               
            Destroy(buffer[0]);
            buffer.RemoveAt(0);
        }
    }

}
