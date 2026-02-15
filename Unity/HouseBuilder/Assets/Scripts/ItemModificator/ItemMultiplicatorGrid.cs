using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ItemMultiplicatorGrid : MonoBehaviour
{
    public GameObject Box;
    public int rows = 4;
    public int columns = 4;
    public float delta_x= 0.0f;
    public float delta_y = 0.3f;
    public float delta_z = 0.3f;

    
    // Start is called before the first frame update
    void Start()
    {
        create_clones();
    }

    // Update is called once per frame
    void Update()
    {

    }

    void create_clones()
    {
        Vector3 start_pos = transform.localPosition;
        for (int r = 0; r < rows; r++)
        {
            for (int c = 0; c < columns; c++)
            {
                Vector3 cloneOffset = new Vector3(c * delta_x, r * delta_y, c*delta_z);
                GameObject clone = Instantiate(Box, transform.position + cloneOffset, transform.rotation);
                clone.transform.SetParent(transform);
            }
        }
    }
}
