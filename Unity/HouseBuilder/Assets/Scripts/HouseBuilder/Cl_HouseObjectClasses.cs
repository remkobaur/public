using System.Collections;
using System.Collections.Generic;
using UnityEngine;


namespace My.HouseCreator{
    
#region Class Floor
    [System.Serializable] 
    public class Cl_Floor : Cl_WallTools
    {
        // public string name = "1st floor";
        // public float height = 2.5f;
        // public Vector3 pos = Vector3.zero;
        // public float wallThickness = 0.2f;
        // public C_Materials materials;

        public List<Cl_Room> rooms = new List<Cl_Room>();  

        public Cl_Floor()
        {
            height = 2.5f;
        }
        public Cl_Floor(string _name,float _height,C_Materials _mat)
        {
            name = _name;
            height = _height;
            materials = _mat;
        }


        public GameObject create(GameObject _parent)
        {
            GameObject go = new GameObject(name);            
            go.transform.parent = _parent.transform;          
            
            //create rooms and inventory tree
            GameObject Inventory = new GameObject("Inventory");
            Inventory.transform.parent = _parent.transform;
            foreach (Cl_Room _room in rooms)
            {
                //create Room
                Transform room_TF = create_room(go, _room);
                //create Inventory GO for room
                GameObject _inv = new GameObject(_room.name);
                _inv.transform.parent = Inventory.transform;
                _inv.transform.position = room_TF.transform.position;
            }

            //Merge meshes with tag "ceiling" in new child
            GameObject ceil = new GameObject("ceiling"); 
            ceil.tag = "ceiling";           
            ceil.transform.parent = go.transform;
            ceil.AddComponent<MeshRenderer>();
            ceil.AddComponent<MeshFilter>();
            MeshCombiner MB = go.AddComponent<MeshCombiner>();
            
            MB.FilterTags.Clear();
            MB.ParentGO = ceil;
            MB.Execute = true;
            MB.FilterTags.Add("ceiling");

            // add Cluster Combiner for rooms to merge Walls, Windows and Floors
            ClusterCombiner CB = go.AddComponent<ClusterCombiner>();
            CB.ClusterTag = "room";
            CB.MeshTags.Clear();
            CB.MeshTags.Add("wall");
            CB.MeshTags.Add("window");
            CB.MeshTags.Add("floor");
            CB.removeEmptyChildren = true;
            // CB.attachRemainingSubChildren = true;
            CB.Execute = true;

            

            
            return go;
        }

        public void clear()
        {
            rooms = new List<Cl_Room>(); 
        } 

        public Vector2 getPosByDirection(string _direction,Cl_Room _room)
        {
            Vector2 _pos = Vector2.zero; 
            switch (_direction)
            {
                case "N":
                    _pos = _room.pos + new Vector2(1f*_room.length, 0f*_room.width)/2f;
                    break;      
                case "S":
                    _pos = _room.pos + new Vector2(-1f*_room.length, 0f*_room.width)/2f;
                    break; 
                case "W":
                    _pos = _room.pos + new Vector2(0f*_room.length,1f*_room.width)/2f;
                    break;                      
                case "E": 
                    _pos = _room.pos + new Vector2(0f*_room.length,-1f*_room.width)/2f;
                    // Debug.Log($"pos_0: {pos} \t|\t new pos: {_pos} \t|\t {_room.width} ");
                    break;                    
                 case "NE":                  
                    _pos = _room.pos + new Vector2(1f*_room.length,-1f*_room.width)/2f;
                    break;                
                case "NW":  
                    _pos = _room.pos + new Vector2(1f*_room.length, 1f*_room.width)/2f;
                    break;      
                case "SE":
                    _pos = _room.pos + new Vector2(-1f*_room.length, -1f*_room.width)/2f;
                    break; 
                case "SW":
                    _pos = _room.pos + new Vector2(-1f*_room.length, 1f*_room.width)/2f;
                    break; 
                default:
                    break;
            }
            return _pos;  

        }
        private Transform create_room(GameObject _parent, Cl_Room _room)
        {
            GameObject room = Cl_MyMaster.createChild(_room.name, _parent);
            room.transform.localPosition = new Vector3(_room.pos.x, 0f, _room.pos.y);
            room.tag = "room";
            GameObject walls = Cl_MyMaster.createChild("walls", room);
            // GameObject inventory = Cl_MyMaster.createChild("inventory", room);
            // add walls with doors and windows
            create_complexWall(0, walls, "N", new Vector2(1, 0), E_wallDir.normal, _room, materials.wall);
            create_complexWall(1, walls, "S", new Vector2(-1, 0), E_wallDir.normal, _room, materials.wall);
            create_complexWall(2, walls, "W", new Vector2(0, 1), E_wallDir.rotated, _room, materials.wall);
            create_complexWall(3, walls, "E", new Vector2(0, -1), E_wallDir.rotated, _room, materials.wall);
            create_complexWall(4, walls, "ceiling", new Vector2(0, 1), E_wallDir.horizontal, _room, materials.wall);
            create_complexWall(5, walls, "floor", new Vector2(0, -1), E_wallDir.horizontal, _room, materials.floor);

            // set Tag for ceiling            
            if (walls.transform.Find("ceiling") != null)
            { walls.transform.Find("ceiling").gameObject.tag = "ceiling"; }

            return room.transform;
        }
        // private void create_complexWall(int ID,GameObject _parent, string _name, Vector2 _pos,string wallType,Cl_Room _room,Material _mat)
        // {
        //     create_wall(ID,_parent,_name,_pos,wallType,_room,_mat);  
        // }
        // private void create_wall(int ID,GameObject _parent, string _name, Vector2 _pos,string wallType,Cl_Room _room,Material _mat)
        // {
        //     if (!_room.activeWalls[ID]){return;}

        //     float d = wallThickness;          
        //     float _yaw = 0f;
        //     float _pitch = 0f;
        //     float _roll = 0f;
        //     float _height = height;
        //     float _length = _room.length;
        //     float _width = _room.width;

        //     Vector3 _pos3 = new Vector3(_pos.x,_height/2f,_pos.y);

        //     Cl_Room tmp = new Cl_Room("tmp",new Vector2(0f,0f));
        //     switch(wallType)
        //     {
        //         case "normal": 
        //             break;
        //         case "rotated":                                       
        //             _yaw =  90f;
        //             _length = _room.width;
        //             _width = _room.length;
        //             break;
        //         case "horizontal":
        //             // _localPos = new Vector3(0f,_pos.y*(height+d)/2+height/2,0f);
        //             // _localScale = new Vector3(_room.length+2f*d,_room.width+2f*d,d);
        //             // _height = _room.width;   
        //             _width = _room.width;
        //             _height = _room.length+2f*d;
        //             _pitch = 90f;
        //             _pos3 = new Vector3(0f,_pos.y*(height+d)/2f + height/2f ,0f);
        //             break;
        //         // case "horizontal2":
        //         //     _localPos = new Vector3(0f,_pos.y*(height+d)/2+height/2,0f);
        //         //     _localScale = new Vector3(_room.length,d,_room.width);
        //         //     break;
        //         default:
        //             break;
        //     }

        //     Quaternion _quat = Quaternion.Euler(_roll,_yaw,_pitch);

        //     Vector3 _localPos = new Vector3(_pos3.x*(_room.length+d)/2f,_pos3.y,_pos3.z*(_room.width+d)/2f);
        //     Vector3 _localScale = new Vector3(d,_height,_width+2f*d);

        //     List<WallModule> _mods = new List<WallModule>(); 
        //     foreach (WallModule _mod in _room.modules)
        //     {
        //         if (_mod.wallName.Equals(_name))
        //         {
        //             _mods.Add(_mod);
        //         }
        //     }
        //     GameObject cube;
        //     if (_mods.Count==0)
        //     {
        //         cube = GameObject.CreatePrimitive(PrimitiveType.Cube); 
        //         if (_mat!=null)
        //         {
        //             cube.GetComponent<MeshRenderer> ().material = _mat;
        //             cube.transform.localScale = _localScale;
        //         }            
        //     }
        //     else
        //     {   
        //         cube = createChild("---",_parent);        
        //         _localPos.y = 0f;       
        //     }

        //     cube.name = _name;
        //     cube.tag="wall";
        //     cube.transform.parent = _parent.transform;             
        //     cube.transform.localRotation = _quat;
        //     cube.transform.localPosition = _localPos;
        //     cube.transform.localRotation = _quat;
        //     cube.transform.localPosition = _localPos;

        //     if (_mods.Count>0)
        //     {   
        //         Vector2 P0 = new Vector2(-(_width+d)/2f,0f);
        //         Vector2 Pe = new Vector2(+(_width+d)/2f,_height);
        //         Vector2 P1,P2,P3,P4;
                
        //         P4 = new Vector2(P0.x,P0.y);
        //         foreach (WallModule _mod in _mods)
        //         {
        //             P1 = new Vector2(_mod.pos_x-_mod.width/2f,Pe.y);
        //             P2 = new Vector2(_mod.pos_x+_mod.width/2f,_mod.pos_y+_mod.height);
        //             P3 = new Vector2(_mod.pos_x-_mod.width/2f,_mod.pos_y);
        //             P4 = new Vector2(_mod.pos_x+_mod.width/2f,P0.y);
        //             // Debug.Log($"mod: \n {_mod.width} \n {P0},{P1},{P2},{P3},{P4},{Pe}");
        //             create_wallParts(cube,P0,P1,_mat,"P0-P1");
        //             create_wallParts(cube,P1,P2,_mat,"P1-P2");
        //             create_wallParts(cube,P3,P4,_mat,"P3-P4");
        //             P0 = P4;

        //             GameObject module = null;
        //             switch(_mod.type)
        //             {
        //                 case ModuleType.Window:
        //                     module = GameObject.CreatePrimitive(PrimitiveType.Cube); 
        //                     module.GetComponent<MeshRenderer> ().material = materials.window;
        //                     module.name = "Window";
        //                     break;
        //                 case ModuleType.Door:
        //                     module = GameObject.CreatePrimitive(PrimitiveType.Cube);                            
        //                     module.GetComponent<MeshRenderer> ().material = materials.door;
        //                     module.name = "Door";
        //                     break;
        //                 case ModuleType.Hole:
        //                     break;
        //                 case ModuleType.Light:
        //                     module = GameObject.CreatePrimitive(PrimitiveType.Cylinder); 
        //                     module.transform.parent = cube.transform;
        //                     module.GetComponent<MeshRenderer> ().material = materials.door;
        //                     module.name = "Light";
        //                     break;
        //                 default:
        //                     break;
        //             }
        //             if (module !=null)
        //             {
        //                 module.transform.parent = cube.transform;
        //                 module.transform.localScale = new Vector3(0.05f,_mod.height,_mod.width);
        //                 module.transform.localPosition = new Vector3(0f,_mod.pos_y+_mod.height/2f,_mod.pos_x);
        //                 module.transform.localRotation = Quaternion.identity;
        //             }
        //         }
        //         create_wallParts(cube,P4,Pe,_mat,"P4-Pe");
        //     }                    

          
            
        // }
        
        // public void create_wallParts(GameObject _parent,Vector2 P1,Vector2 Pe,Material _mat,string _name = "WallPart")
        // {
        //     if ( Mathf.Abs(Pe.y-P1.y)<0.001)
        //     {return;}
        //     GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube); 
        //     cube.name = _name;
        //     // cube.tag="wall";
        //     cube.transform.parent = _parent.transform; 
        //     cube.transform.localPosition = new Vector3( 0f , (Pe.y+P1.y)/2f,(Pe.x+P1.x)/2f ) ; 
        //     cube.transform.localScale = new Vector3( wallThickness , Mathf.Abs(Pe.y-P1.y),Mathf.Abs(Pe.x-P1.x)) ; 
        //     cube.transform.localRotation = Quaternion.identity;
        //     if (_mat!=null)
        //     {
        //         cube.GetComponent<MeshRenderer> ().material = _mat;
        //     }
        // }

        public void setActiveWalls(int id,bool status)
        {
            foreach(Cl_Room _room in rooms)
            {
                _room.activeWalls[id] = status;
            }
        }
    } // end class

#endregion


#region Class Room
    [System.Serializable] 
    public class Cl_Room    {
        
        public string name = "Room";
        public float length = 4f;
        public float width = 3f;
        public Vector2 pos = Vector2.zero;

        public RelPlacement relPlace = new RelPlacement();
        public bool[] activeWalls = {true,true,true,true,true,true};
        public List<WallModule> modules = new List<WallModule>();

         
        public Cl_Room(string _name,Vector2 _pos, float _length = 4f,float _width=3f)
        {
            name = _name;
            length = _length;
            width = _width;
            pos = _pos;
            
        }  

        public void addModule(WallModule module)
        {
            modules.Add(module);
        }  
        public void addDoor(string _direction,float xOff=0f)
        {
            addModule(new WallModule(_direction,ModuleType.Door,new Rect(xOff,0f,0.8f,2f)))  ; 
        }
        public void addWindow(string _direction,float xOff=0f)
        {
            addModule(new WallModule(_direction,ModuleType.Window,new Rect(xOff,0.6f,1f,1f)))  ; 
        }
        public void addLight(string _direction = "ceiling",float xOff=0f,float yOff=0f)
        {
            addModule(new WallModule(_direction,ModuleType.Light,new Rect(xOff,yOff,0.2f,0.2f)))  ; 
        }
        public void place(Cl_Floor _floor)
        {
            place(_floor,relPlace.refRoomName, relPlace.direction);
        } 
        public void place(Cl_Floor _floor,string _refRoomName, string _direction)
        {
            Cl_Room _refRoom = null;
            Vector2 _ref = Vector2.zero;
            Vector2 _pos = Vector2.zero;

            relPlace.refRoomName = _refRoomName;
            relPlace.direction = _direction;

            // find refRoom            
            foreach (Cl_Room _room in _floor.rooms)
            {
                if (_room.name.Equals(relPlace.refRoomName))
                {
                    _refRoom = _room;
                    // Debug.LogWarning($"Room <{name}> :: RefRoom <{relPlace.refRoomName}> found. --> Size = {_refRoom.length} x {_refRoom.width}");
                    break;
                }
            }
            if (_refRoom == null)
            {
                Debug.LogWarning($"Room <{name}> :: RefRoom <{relPlace.refRoomName}> was not found in room list. --> Relative placement is skipped!");
                return;
            }

            Vector2 wall_x = new Vector2(_floor.wallThickness,0f);
            Vector2 wall_y = new Vector2(0f,_floor.wallThickness);
            pos = Vector2.zero;
            switch(relPlace.direction)
            {
                case "N":
                    _ref = _floor.getPosByDirection("N",_refRoom);
                    _pos = _ref+_floor.getPosByDirection("S",this) + wall_x + relPlace.offset;
                    break;      
                case "S":
                     _ref = _floor.getPosByDirection("S",_refRoom);
                    _pos = _ref+_floor.getPosByDirection("N",this) - wall_x + relPlace.offset;
                    break; 
                case "W":
                    _ref = _floor.getPosByDirection("W",_refRoom);
                    _pos = _ref+_floor.getPosByDirection("E",this) + wall_y + relPlace.offset;
                    break;                      
                case "E":
                    _ref = _floor.getPosByDirection("E",_refRoom);
                    _pos = _ref-_floor.getPosByDirection("W",this) - wall_y + relPlace.offset;
                    // Debug.Log($"ref: {_ref} \t|\t pos: {_pos}");
                    break;    
                
                 case "NE":
                    _ref = _floor.getPosByDirection("NE",_refRoom);
                    _pos = _ref-_floor.getPosByDirection("SE",this) + wall_x  + relPlace.offset;
                    break;            
                case "NW":  
                    _ref = _floor.getPosByDirection("NW",_refRoom);
                    _pos = _ref-_floor.getPosByDirection("SW",this) + wall_x  + relPlace.offset;                 
                    break;      
                case "SE":  
                    _ref = _floor.getPosByDirection("SE",_refRoom);
                    _pos = _ref-_floor.getPosByDirection("NE",this) - wall_x  + relPlace.offset;                  
                    break; 
                case "SW": 
                    _ref = _floor.getPosByDirection("SW",_refRoom);
                    _pos = _ref-_floor.getPosByDirection("NW",this) - wall_x  + relPlace.offset;                   
                    break; 
                
                case "EN":     
                    _ref = _floor.getPosByDirection("NE",_refRoom);
                    _pos = _ref-_floor.getPosByDirection("NW",this) - wall_y  + relPlace.offset;                 
                    break;                
                case "WN": 
                    _ref = _floor.getPosByDirection("NW",_refRoom);
                    _pos = _ref-_floor.getPosByDirection("NE",this) + wall_y  + relPlace.offset;                         
                    break;      
                case "ES":      
                    _ref = _floor.getPosByDirection("SE",_refRoom);
                    _pos = _ref-_floor.getPosByDirection("SW",this) - wall_y  + relPlace.offset;                    
                    break; 
                case "WS":           
                    _ref = _floor.getPosByDirection("SW",_refRoom);
                    _pos = _ref-_floor.getPosByDirection("SE",this) + wall_y  + relPlace.offset;         
                    break; 
                 
                default:
                    _ref = _refRoom.pos;
                    break;
            }
            pos = _pos;            
        }   
        
    } // end class
#endregion

#region RelPlacement
    [System.Serializable] 
    public class RelPlacement
    {
        public string refRoomName = "";
        public string direction = "N";    
        public Vector2 offset = Vector2.zero;        
    }
#endregion

#region Class WallModule

    public enum ModuleType
    {
        Hole,
        Door,
        Window,            
        Light
    }

    [System.Serializable]  
    public class WallModule
    {       
        public string wallName = "";
        public ModuleType type = ModuleType.Hole;        
        public float pos_x = 0f;
        public float pos_y = 0f;
        public float width = 0f;
        public float height = 0f;
        //public Rect rect = new Rect(0f,0f,0f,0f);

        public WallModule(string _wallName,ModuleType _type,Rect _rect)
        {
            wallName = _wallName;
            type = _type;
            pos_x = _rect.x;
            pos_y = _rect.y;
            width = _rect.width;
            height = _rect.height;
        }
    } // end class
#endregion

#region Class Materials
    [System.Serializable] 
    public class C_Materials
    {
        public Material wall = null;
        public Material floor = null;
        public Material door = null;
        public Material window = null;

        // public C_Materials()
        // {
        //     init();
        // }
        public C_Materials(Material _wall, Material _floor, Material _door,Material _window)
        {
            wall = _wall;
            floor = _floor;
            door = _door;
            window = _window;
        }
        public void init()
        {
            wall = (Material)Resources.Load("Materials/Rooms/wall_white", typeof(Material));
            floor = (Material)Resources.Load("Materials/Rooms/floor_wood", typeof(Material));
            door = (Material)Resources.Load("Materials/Rooms/door_red", typeof(Material));
            window = (Material)Resources.Load("Materials/Rooms/window_glass", typeof(Material));
        }
    } // end class
} // end namespace
#endregion
