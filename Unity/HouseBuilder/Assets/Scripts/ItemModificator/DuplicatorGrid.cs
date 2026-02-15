using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DuplicatorGrid : MonoBehaviour
{
    public enum ColorMixTypes
    {
        rows,cols,stack,mixed        
    }
    public GameObject originalObject;
    [Header("Stack Settings")]
    public int block_amount = 1;
    public float obj_dx = 0.0f;
    public float obj_dz = 0.1f;

    [Header("Raster Settings")]
    public int rows = 4;
    public int columns = 4;
    public float delta_x= 0.0f;
    public float delta_y = 0.35f;
    public float delta_z = 0.37f;
    public bool skip_first = true;

    [Header("Material Settings")]
    public bool change_materials = true;
    public string childName = null;
    public ColorMixTypes mix_type = new ColorMixTypes();
    public Material[] myMaterials = new Material[5];
    

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
        for (int n = 0; n < block_amount; n++)
        {
            for (int r = 0; r < rows; r++)
            {
                for (int c = 0; c < columns; c++)
                {
                    GameObject clone;
                    if (skip_first && c == 0 && r == 0 && n == 0)
                    {
                        clone = originalObject;
                    }
                    else
                    {
                        Vector3 cloneOffset = new Vector3(c * delta_x + obj_dx * n, r * delta_y, c * delta_z + obj_dz * n);
                        //create clone at desired position
                        clone = Instantiate(originalObject, transform.position + cloneOffset, transform.rotation);
                        //set parent
                        clone.transform.SetParent(transform);
                    }
                    
                    //change material by row
                    if (change_materials)
                    {
                        Material newMaterial = null;
                        switch (mix_type)
                        {
                            case ColorMixTypes.rows: newMaterial = myMaterials[r]; break;
                            case ColorMixTypes.cols: newMaterial = myMaterials[c]; break;
                            case ColorMixTypes.stack: newMaterial = myMaterials[n]; break;
                            case ColorMixTypes.mixed:  newMaterial = myMaterials[Random.Range(0, myMaterials.Length)]; break;
                        }
                        
                        
                        if (childName == null)
                        {
                            clone.GetComponent<Renderer>().material = newMaterial;
                        }
                        else
                        {
                            Transform childTransform = clone.transform.Find(childName);
                            if (childTransform != null)
                            {
                                childTransform.gameObject.GetComponent<Renderer>().material = newMaterial;
                            }
                        }                        
                    }
                }
            }
        }
    }
}
