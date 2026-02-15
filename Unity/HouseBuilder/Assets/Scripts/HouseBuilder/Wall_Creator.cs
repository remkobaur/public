using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]
public class Wall_Creator : MonoBehaviour
{
    public virtual void Start()
    {}  

    public GameObject createParent(string _name)
    {
        GameObject go = new GameObject(_name);
        //go.name = _name
        return go;
    }
    
    public GameObject createWall(string _name, GameObject _parent,Vector3 _pos,Vector3 _scale, Material _mat=null)
    {        
        GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
        cube.name = _name;
        cube.transform.parent = _parent.transform;
        cube.transform.localPosition = _pos;
        cube.transform.localScale = _scale;
        if (_mat!=null)
        {
            cube.GetComponent<MeshRenderer> ().material = _mat;
        }

        return cube;
    }

    public GameObject addLight(GameObject _parent,Vector3 _pos)
    {
         // Make a game object
        GameObject lightGameObject = new GameObject("The Light");
        lightGameObject.transform.parent = _parent.transform;

        // Add the light component
        Light lightComp = lightGameObject.AddComponent<Light>();
        lightComp.type = LightType.Point;
        lightComp.spotAngle = 120f;

        // Set color and position
        //lightComp.color = Color.blue;

        // Set the position (or any transform property)
        lightGameObject.transform.position = _pos;
        return lightGameObject;
    }
}
