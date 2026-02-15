using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]
public class Room_Creator : Wall_Creator
{    
    public bool createObjects=false;
    public Material mat_floor = null;
    public Material mat_wall = null;

    // Start is called before the first frame update
    public override void Start()
    {
        //base.Start();
    }
    
    // Update is called once per frame
    public void Update()
    {
        if (createObjects)
        {
            createObjects = false;
            exec_create_objects();
        }           
    }

    public void exec_create_objects()
    {
        Vector3 size = new Vector3(4.5f, 2.50f, 3.0f);
        Vector3 pos = new Vector3(0.0f, 0.0f, 0.0f);
        float wallThickness = 0.2f;

        GameObject _room= createRoom("Walls",gameObject, pos, size, wallThickness );
    }

    private GameObject createRoom(string _name, GameObject _parent, Vector3 _pos, Vector3 _size,float wallThickness)
    {
        GameObject go = createParent(_name);
        go.transform.parent = _parent.transform;
  
        // front back
        createWall("Wall_N",go, new Vector3( (_size.x+wallThickness)/2.0f , _size.y/2f, 0f),new Vector3(wallThickness, _size.y, _size.z+2*wallThickness),mat_wall);
        createWall("Wall_S",go, new Vector3(-(_size.x+wallThickness)/2.0f , _size.y/2f, 0f),new Vector3(wallThickness, _size.y, _size.z+2*wallThickness),mat_wall);
        // left / right
        createWall("Wall_W",go, new Vector3(0f , _size.y/2f,  (_size.z+wallThickness)/2.0f),new Vector3(_size.x+2*wallThickness, _size.y, wallThickness),mat_wall);
        createWall("Wall_E",go, new Vector3(0f , _size.y/2f, -(_size.z+wallThickness)/2.0f),new Vector3(_size.x+2*wallThickness, _size.y, wallThickness),mat_wall);
        // top / bottom
        Vector3 hor_scale = new Vector3(_size.x+2f*wallThickness, wallThickness , _size.z+2f*wallThickness);
        createWall("Ceiling",go, new Vector3(0f , _size.y+wallThickness/2f, 0f),hor_scale,mat_wall);
        createWall("Floor",go, new Vector3(0f , -wallThickness/2f, 0f),hor_scale,mat_floor);

        // add light
        addLight(_parent,new Vector3(0f,_size.y-0.01f,0f));
        return go;
    }
    
    
}
