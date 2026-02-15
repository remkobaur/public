using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.IO;
using System.Linq;

namespace My.ns_Furniture {


    #region enums
    public enum E_BoardDir
    {
        front, door,doorRot,
        vertical,
        horizontal
    }
    public enum e_doorType
    {
        none,
        left,
        right,
        both,
        down,
        drawer
        };
    public enum E_Furniture
    {
        None,
        Expedit_4x4,
        Kallax_2x2,
        Kallax_4x4,
        Pax_1mx2m,
        Shelf_3x3,
        Kitchen_80x70,
        Kitchen_40x70,
        Kitchen_60x70
    }

    #endregion

    #region Main Class
    [ExecuteInEditMode]
    public class FurnitureCreator : MonoBehaviour
    {
        #region properties


        [Header("Module ACTION")]
        public bool ButtonCreateShelf = false;
        public bool ButtonCreateExamples = false;
        public bool ButtonDestroyAllChildren = false;

        [Header("Materials")]
        public Material material;

        public GameObject handle = null;
        public GameObject front = null;

        [Header("Update Child Materials")]
        public Material materialBoards=null;
        public Material materialDoor=null;
        public Material materialHandle=null;
        public bool updateMaterials = false;

        [Header("Furniture")]
        public bool enableMergeMeshes = true;
        public E_Furniture Template = E_Furniture.None;

        public Cl_Furniture furniture = new Cl_Furniture();

        [Header("Json Settings")]
        public string jsonFile = "Furniture.json";
        public bool ButtonJsonImport = false;
        public bool ButtonJsonExport = false;

        public GameObject furnGO = null;

        #endregion

        #region main
        // Start is called before the first frame update

        void Start()
        {

        }

        // Update is called once per frame
        void Update()
        {
            ButtonActions();
        }
        #endregion

        #region actions and callbacks
        private void ButtonActions()
        {
            furniture.enableMergeMeshes = enableMergeMeshes;
            if (ButtonCreateShelf)
            {
                ButtonCreateShelf = false;
                if (furnGO == null)
                {
                    furnGO = new GameObject(furniture.name);
                    furnGO.transform.parent = transform;
                    furnGO.transform.localPosition = Vector3.zero;
                }

                furniture.material = material;
                furniture.construct_shelf();
                // furnGO = furniture.create_furniture(furnGO, front, handle);
                furniture.create_furniture(furnGO, front, handle);
            }
            if (ButtonCreateExamples)
            {
                ButtonCreateExamples = false;
                init_furniture();
            }
            if (ButtonDestroyAllChildren)
            {
                ButtonDestroyAllChildren = false;
                Cl_MyMaster.destroyAllChildren(gameObject);
            }
            //update child matierals
            if (updateMaterials)
            {
                updateMaterials = false;
                SetMaterialForAllChilds[] SMFCs = GetComponentsInChildren<SetMaterialForAllChilds>();
                foreach (SetMaterialForAllChilds smfc in SMFCs)
                {
                    smfc.materialBoards = materialBoards;
                    smfc.materialDoor = materialDoor;
                    smfc.materialHandle = materialHandle;
                    smfc.Execute=true;
                }
            }

            // json
                if (ButtonJsonImport)
                {
                    ButtonJsonImport = false;
                    json_import(jsonFile);
                }
            if (ButtonJsonExport)
            {
                ButtonJsonExport = false;
                json_export(jsonFile);
            }
        }
        #endregion
        public void init_furniture()
        {
            switch (Template)
            {
                case E_Furniture.None:
                    furniture = new Cl_Furniture();
                    break;
                case E_Furniture.Kallax_2x2:
                    furniture = new Cl_Furniture("Kallax_2x2", 0.765f, 0.765f, 0.392f, 0.037f, 0.016f, 2, 2, 0f);
                    break;
                case E_Furniture.Kallax_4x4:
                    furniture = new Cl_Furniture("Kallax_4x4", 1.50f, 1.50f, 0.392f, 0.037f, 0.016f, 4, 4, 0f);
                    break;
                case E_Furniture.Pax_1mx2m:
                    furniture = new Cl_Furniture("Pax_1mx2m", 2.02f, 1f, 0.58f, 0.018f, 0.018f, 5, 1, 0.07f, new Vector3(0.05f,0.8f,0.0f),e_doorType.both);
                    break;
                case E_Furniture.Expedit_4x4:
                    furniture = new Cl_Furniture("Expedit_4x4", 1.50f, 1.50f, 0.392f, 0.050f, 0.016f, 4, 4, 0f);
                    break;
                case E_Furniture.Shelf_3x3:
                    furniture = new Cl_Furniture("Shelf_3x3", 1.05f, 1.05f, 0.33f, 0.0150f, 0.015f, 3, 3, 0f);
                    break;
                case E_Furniture.Kitchen_40x70:
                    furniture = new Cl_Furniture("Kitchen_40x70", 0.70f, 0.40f, 0.40f, 0.0150f, 0.015f, 3, 1, 0f, new Vector3(0.05f,0.1f,0.0f),e_doorType.left);
                    break;
                case E_Furniture.Kitchen_60x70:
                    furniture = new Cl_Furniture("Kitchen_60x70", 0.70f, 0.60f, 0.40f, 0.0150f, 0.015f, 3, 1, 0f, new Vector3(0.05f,0.1f,0.0f),e_doorType.left);
                    break;
                case E_Furniture.Kitchen_80x70:
                    furniture = new Cl_Furniture("Kitchen_80x70", 0.70f, 0.80f, 0.40f, 0.0150f, 0.015f, 3, 1, 0f, new Vector3(0.05f,0.1f,0.0f),e_doorType.both);
                    break;
                default:
                    furniture = new Cl_Furniture();
                    break;
            }
        }

        #region JSON
        public void json_export(string _jsonFile = "Furniture.json", string _jsonPath = "json")
        {
            string jsonText = JsonUtility.ToJson(furniture, true);
            System.IO.File.WriteAllText(Path.Combine(Application.streamingAssetsPath, _jsonPath, _jsonFile), jsonText);
        }
        public void json_import(string _jsonFile = "Furniture.json", string _jsonPath = "json")
        {
            // Debug.Log(Path.Combine(Application.streamingAssetsPath,_jsonPath,_jsonFile));
            string jsonText = System.IO.File.ReadAllText(Path.Combine(Application.streamingAssetsPath, _jsonPath, _jsonFile));
            furniture = JsonUtility.FromJson<Cl_Furniture>(jsonText);
        }
        #endregion        
    }
    #endregion // end main class

    #region Class Board
    public class Cl_Board
    {
        public string name;
        public Vector3 pos;
        public float length;
        public float width;
        public float thickness;
        public E_BoardDir boardType;
        public Vector3 handlePos;
        public e_doorType doorType = e_doorType.left;

        public Cl_Board(string _name, Vector3 _pos, float _length, float _width, float _thickness, E_BoardDir _boardType, Vector3? _handlePos = null,e_doorType? _doorType = null)
        {
            name = _name;
            pos = _pos;
            length = _length;
            width = _width;
            boardType = _boardType;
            thickness = _thickness;
            if (_handlePos == null) { handlePos = new Vector3(0f, 0f, 0f); }
            else  { handlePos = (Vector3)_handlePos;  }
            if (_doorType == null) { doorType = e_doorType.none; }
            else  { doorType = (e_doorType)_doorType;  }
        }
    }
    #endregion

    #region Class Furniture
    [System.Serializable] 
    public class Cl_Furniture 
    {
        public string name = "";
        public float height = 1f;
        public float width = 1f;
        public float depth = 1f;     
        public Vector3 posOffset = Vector3.zero;   
        public float thickFrame = 0.02f;
        public float thickBoard = 0.02f;
        public int rows = 5;
        public int cols = 1;
        public float footbarHeight = 0.00f;
        public Material material = null;
        public bool enableMergeMeshes = true;

        public int num_doors = 0;
        public Vector3 handleOffset = Vector3.zero;
        public e_doorType doorType = e_doorType.left;
        
        
        public List<Cl_Board> boards = new List<Cl_Board>();

        public Cl_Furniture()
        {
            // name  = "None";
            // height = 2f;
            // width  = 1.0f;
            // depth  = 0.5f;
            
            // thickFrame =0.02f;
            // thickBoard =0.02f;
            // rows = 1;
            // cols = 1; 
        }
        public Cl_Furniture(string _name = "Regal", float _height = 1.50f, float _width = 0.6f, float _depth = 0.4f, float _thickFrame = 0.02f, float _thickBoard = 0.02f, int _rows = 5, int _cols = 1, float _footbarHeight = 0f, Vector3? _handleOffset = null, e_doorType? _doorType = null)
        {
            name = _name;
            width = _width;
            depth = _depth;
            height = _height;
            thickFrame = _thickFrame;
            thickBoard = _thickBoard;
            rows = _rows;
            cols = _cols;
            footbarHeight = _footbarHeight;
            if (_handleOffset == null) { handleOffset = Vector3.zero; }
            else { handleOffset = (Vector3)_handleOffset; }
            if (_doorType == null) { doorType = e_doorType.none; }
            else{ doorType = (e_doorType)_doorType; }
        }
        public void construct_shelf()
        {
            // clear old list
            boards = new List<Cl_Board>();

            // create frame
            // boards.Add(new Cl_Board("normal",new Vector2(0f,0f*height),depth,thickFrame,width,E_BoardDir.normal));
            boards.Add(new Cl_Board("bottom",   new Vector3(0f,0f*height+thickFrame/2f+footbarHeight),depth,thickFrame,width,E_BoardDir.horizontal));
            boards.Add(new Cl_Board("top",      new Vector3(0f,1f*height-thickFrame/2f),depth,thickFrame,width,E_BoardDir.horizontal));
            boards.Add(new Cl_Board("left",     new Vector3(0f,height/2f,(width-thickFrame)/2f),depth,thickFrame,height,E_BoardDir.vertical));
            boards.Add(new Cl_Board("right",    new Vector3(0f,height/2f,-(width-thickFrame)/2f),depth,thickFrame,height,E_BoardDir.vertical));
            boards.Add(new Cl_Board("footbar",  new Vector3((depth-thickFrame)/2f,footbarHeight/2f),footbarHeight,thickFrame,width,E_BoardDir.front));

            // add doors
            switch (doorType)
            {
                case e_doorType.none:
                    break;
                case e_doorType.left:
                    boards.Add(new Cl_Board("door_left", new Vector3((depth + thickFrame) / 2f, height / 2f, 0), height, thickFrame, width - 0.002f, E_BoardDir.door,new Vector3(depth/2f+thickFrame+handleOffset.z,handleOffset.y, ( width / 2f - handleOffset.x))));
                    break;
                case e_doorType.right:
                    boards.Add(new Cl_Board("door_right", new Vector3((depth + thickFrame) / 2f, height / 2f, 0), height, thickFrame, width - 0.002f, E_BoardDir.door,new Vector3(depth/2f+thickFrame+handleOffset.z,handleOffset.y, (-width / 2f + handleOffset.x))));
                    break;
                case e_doorType.both:
                    boards.Add(new Cl_Board("door_left", new Vector3((depth + thickFrame) / 2f, height / 2f, -width * 1f / 4f), height, thickFrame, width / 2f - 0.002f, E_BoardDir.door,new Vector3(depth/2f+thickFrame+handleOffset.z,handleOffset.y,-handleOffset.x)));
                    boards.Add(new Cl_Board("door_right", new Vector3((depth + thickFrame) / 2f, height / 2f, width * 1f / 4f), height, thickFrame, width / 2f - 0.002f, E_BoardDir.door,
                    new Vector3(depth / 2f + thickFrame + handleOffset.z, handleOffset.y, handleOffset.x)));
                    break;
                case e_doorType.down:
                    boards.Add(new Cl_Board("door_down", new Vector3((depth + thickFrame) / 2f, height / 2f, 0), height, thickFrame, width - 0.002f, E_BoardDir.doorRot,
                    new Vector3(depth / 2f + thickFrame + handleOffset.z, (height- handleOffset.x), 0.0f)));
                    break;
                case e_doorType.drawer:
                    boards.Add(new Cl_Board("drawer", new Vector3((depth + thickFrame) / 2f, height / 2f, 0), height, thickFrame, width - 0.002f, E_BoardDir.doorRot,
                    new Vector3(depth / 2f + thickFrame + handleOffset.z, handleOffset.y, handleOffset.x)));
                    break;

                default:
                    Debug.LogError("num_doors must have a value in Range of [0,1,2] for furniture " + name);
                    break;  
            }
            // add boards in the middle
                for (int k = 0; k < (rows - 1f); k++)
                {
                    float y = (float)(k + 1) * (height - 2f * thickFrame - footbarHeight) / (rows) + thickFrame + footbarHeight;
                    boards.Add(new Cl_Board($"Hboard{k}", new Vector3(0f, y, 0f), depth, thickBoard, width - 2f * thickFrame, E_BoardDir.horizontal));
                }
            for (int k=0;k<(cols-1f);k++)
            {
                float x = (float)(k+1)*((width-2f*thickFrame)/(float)cols);
                boards.Add(new Cl_Board($"Vboard{k}",new Vector3(0f,height/2f,x-(width/2f-thickFrame)),depth,thickBoard,height-2f*thickFrame,E_BoardDir.vertical));
            }
        }
        public GameObject create_furniture(GameObject shelf = null, GameObject _front = null, GameObject _handle = null)
        {
            if (shelf == null) {shelf = new GameObject(name);}

            foreach (Cl_Board board in boards)
            {
                create_board(shelf, board, _front, _handle);
            }

            shelf.AddComponent<SetMaterialForAllChilds>();
            
            shelf.AddComponent<Furniture>();
            MeshCombiner MC = shelf.AddComponent<MeshCombiner>();
            MC.ParentGO = shelf;
            MC.FilterTags.Add("board");
            shelf.GetComponent<Furniture>().properties = this;           
            if (enableMergeMeshes)
            {
                MC.Execute = true;
            }

            Inventory inv = shelf.AddComponent<Inventory>();
            inv.N_objects = rows * cols;
            // inv.init();  // it's buggy --> all children will be destroyed
            return shelf;               
        }

        public void create_board(GameObject _parent, Cl_Board _board, GameObject _front, GameObject _handle)
        {
            float d = _board.thickness;
            float _yaw = 0f;
            float _pitch = 0f;
            float _roll = 0f;

            switch (_board.boardType)
            {
                case E_BoardDir.front:
                    _yaw = 90f;
                    _pitch = 90f;
                    break;
                case E_BoardDir.door:
                    _yaw = 90f;
                    _pitch = 90f;                    
                    break;
                case E_BoardDir.doorRot:
                    _yaw = 90f;
                    _pitch = 90f;                    
                    break;
                case E_BoardDir.vertical:
                    break;
                case E_BoardDir.horizontal:
                    _roll = 90f;
                    break;
                default:
                    break;
            } 

            GameObject b;
            Vector3 _scale;

            if (_front != null && (_board.boardType == E_BoardDir.door ||_board.boardType == E_BoardDir.doorRot))
            {
                b = MonoBehaviour.Instantiate(_front);
                _scale = b.transform.localScale;                
            }
            else
            {
                b = GameObject.CreatePrimitive(PrimitiveType.Cube);
                b.GetComponent<MeshRenderer>().material = material;
                _scale = new Vector3(_board.length, _board.thickness, _board.width);
            }
            

            b.name = _board.name;
            b.tag = "board";

            b.transform.parent = _parent.transform;
            b.transform.localRotation = Quaternion.Euler(_roll, _yaw, _pitch);
            b.transform.localScale = _scale;
            
            // b.transform.localPosition = new Vector3(_board.pos.x+_board.width/2f,_board.pos.y,_board.pos.z);
            b.transform.localPosition = new Vector3(_board.pos.x, _board.pos.y, _board.pos.z);

            //add handle
            if (_board.boardType == E_BoardDir.door || _board.boardType == E_BoardDir.doorRot)
            {

                b.tag = "door";
                if (_board.handlePos != Vector3.zero && _handle != null)
                {
                    GameObject go_handle = MonoBehaviour.Instantiate(_handle);
                    go_handle.transform.parent = _parent.transform;
                    go_handle.transform.localPosition = _board.handlePos;
                    go_handle.transform.rotation = b.transform.rotation;
                    if (_board.boardType == E_BoardDir.doorRot)
                    {
                        go_handle.transform.Rotate(new Vector3(0.0f,0.0f,90.0f));
                    }                   
                    go_handle.transform.parent = b.transform;
                    go_handle.tag = "handle";
                }   
            }
        }   

    }
#endregion Class Furniture


} // end namespace
