using System.Collections;
using System.Collections.Generic;
using UnityEngine;

#region Class WallTools

namespace My.HouseCreator{

    public enum E_wallDir
    {
        normal,
        rotated,
        horizontal
    }

    public class Cl_WallTools
    {
        public string name = "1st floor";
        public float height = 2.5f;
        public Vector3 pos = Vector3.zero;
        public float wallThickness = 0.2f;
        public C_Materials materials;

        public GameObject createChild(string _name,GameObject _parent)
        {
            GameObject go = new GameObject(_name);
            go.transform.parent = _parent.transform;
            go.transform.localPosition = Vector3.zero;
            //go.name = _name
            return go;
        }
        public void create_complexWall(int ID,GameObject _parent, string _name, Vector2 _pos,E_wallDir wallType,Cl_Room _room,Material _mat)
        {
            create_wall(ID,_parent,_name,_pos,wallType,_room,_mat);  
        }
        public void create_wall(int ID,GameObject _parent, string _name, Vector2 _pos,E_wallDir wallType,Cl_Room _room,Material _mat)
        {
            if (!_room.activeWalls[ID]){return;}

            float d = wallThickness;          
            float _yaw = 0f;
            float _pitch = 0f;
            float _roll = 0f;
            float _height = height;
            float _length = _room.length;
            float _width = _room.width;

            Vector3 _pos3 = new Vector3(_pos.x,_height/2f,_pos.y);

            Cl_Room tmp = new Cl_Room("tmp",new Vector2(0f,0f));
            switch(wallType) 
            {
                case E_wallDir.normal: 
                    break;
                case E_wallDir.rotated:                                       
                    _yaw =  90f;
                    _length = _room.width;
                    _width = _room.length;
                    break;
                case E_wallDir.horizontal:
                    // _localPos = new Vector3(0f,_pos.y*(height+d)/2+height/2,0f);
                    // _localScale = new Vector3(_room.length+2f*d,_room.width+2f*d,d);
                    // _height = _room.width;   
                    _width = _room.width;
                    _height = _room.length+2f*d;
                    _pitch = 90f;
                    _pos3 = new Vector3(0f,_pos.y*(height+d)/2f + height/2f ,0f);
                    break;
                // case "horizontal2":
                //     _localPos = new Vector3(0f,_pos.y*(height+d)/2+height/2,0f);
                //     _localScale = new Vector3(_room.length,d,_room.width);
                //     break;
                default:
                    break;
            }

            Quaternion _quat = Quaternion.Euler(_roll,_yaw,_pitch);

            Vector3 _localPos = new Vector3(_pos3.x*(_room.length+d)/2f,_pos3.y,_pos3.z*(_room.width+d)/2f);
            Vector3 _localScale = new Vector3(d,_height,_width+2f*d);

            List<WallModule> _mods = new List<WallModule>(); 
            foreach (WallModule _mod in _room.modules)
            {
                if (_mod.wallName.Equals(_name))
                {
                    _mods.Add(_mod);
                }
            }
            GameObject cube;
            if (_mods.Count==0)
            {
                cube = GameObject.CreatePrimitive(PrimitiveType.Cube); 
                if (_mat!=null)
                {
                    cube.GetComponent<MeshRenderer> ().material = _mat;                    
                }    
                cube.transform.localScale = _localScale;        
            }
            else
            {   
                cube = createChild("---",_parent);        
                _localPos.y = 0f;       
            }

            cube.name = _name;
            cube.tag="wall";
            cube.transform.parent = _parent.transform;             
            cube.transform.localRotation = _quat;
            cube.transform.localPosition = _localPos;
    

            if (_mods.Count>0)
            {   
                Vector2 P0 = new Vector2(-(_width+d)/2f,0f);
                Vector2 Pe = new Vector2(+(_width+d)/2f,_height);
                Vector2 P1,P2,P3,P4;
                
                P4 = new Vector2(P0.x,P0.y);
                foreach (WallModule _mod in _mods)
                {
                    P1 = new Vector2(_mod.pos_x-_mod.width/2f,Pe.y);
                    P2 = new Vector2(_mod.pos_x+_mod.width/2f,_mod.pos_y+_mod.height);
                    P3 = new Vector2(_mod.pos_x-_mod.width/2f,_mod.pos_y);
                    P4 = new Vector2(_mod.pos_x+_mod.width/2f,P0.y);
                    // Debug.Log($"mod: \n {_mod.width} \n {P0},{P1},{P2},{P3},{P4},{Pe}");
                    create_wallParts(cube,P0,P1,_mat,"P0-P1");
                    create_wallParts(cube,P1,P2,_mat,"P1-P2");
                    create_wallParts(cube,P3,P4,_mat,"P3-P4");
                    P0 = P4;

                    GameObject module = null;
                    switch(_mod.type)
                    {
                        case ModuleType.Window:
                            module = GameObject.CreatePrimitive(PrimitiveType.Cube); 
                            module.GetComponent<MeshRenderer> ().material = materials.window;
                            module.name = "Window";
                            module.tag = "window";
                            break;
                        case ModuleType.Door:
                            module = GameObject.CreatePrimitive(PrimitiveType.Cube);                            
                            module.GetComponent<MeshRenderer> ().material = materials.door;
                            module.name = "Door_"+_room.name;
                            module.tag = "door";
                            break;
                        case ModuleType.Hole:
                            break;
                        case ModuleType.Light:
                            module = GameObject.CreatePrimitive(PrimitiveType.Cylinder); 
                            module.transform.parent = cube.transform;
                            module.GetComponent<MeshRenderer> ().material = materials.door;
                            module.name = "Light";
                            break;
                        default:
                            break;
                    }
                    if (module !=null)
                    {
                        module.transform.parent = cube.transform;
                        module.transform.localScale = new Vector3(0.05f,_mod.height,_mod.width);
                        module.transform.localPosition = new Vector3(0f,_mod.pos_y+_mod.height/2f,_mod.pos_x);
                        module.transform.localRotation = Quaternion.identity;
                    }
                }
                create_wallParts(cube,P4,Pe,_mat,"P4-Pe");
            }       
        } 
        
        public void create_wallParts(GameObject _parent,Vector2 P1,Vector2 Pe,Material _mat,string _name = "WallPart")
        {
            if ( Mathf.Abs(Pe.y-P1.y)<0.001)
            {return;}
            GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube); 
            cube.name = _name;
            // cube.tag="wall";
            cube.transform.parent = _parent.transform; 
            cube.transform.localPosition = new Vector3( 0f , (Pe.y+P1.y)/2f,(Pe.x+P1.x)/2f ) ; 
            cube.transform.localScale = new Vector3( wallThickness , Mathf.Abs(Pe.y-P1.y),Mathf.Abs(Pe.x-P1.x)) ; 
            cube.transform.localRotation = Quaternion.identity;
            cube.tag = "wall";
            if (_mat != null)
            {
                cube.GetComponent<MeshRenderer>().material = _mat;
            }
        }
    } // end class
} // end namespace
#endregion

