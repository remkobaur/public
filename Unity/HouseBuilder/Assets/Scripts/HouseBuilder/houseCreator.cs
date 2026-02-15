using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.IO;
using System.Linq;

namespace My.HouseCreator{
    #region Main Class
    


    [ExecuteInEditMode]   
    public class houseCreator : MonoBehaviour
    {    
        public enum ToggleTags{
            ceiling,
            door,
            window
        }

        #region properties
        [Header("Json Settings")]
        public string jsonFile = "Floor.json";
        public string jsonPath = Path.Combine("StreamingAssets","json");


        [Header("ACTION")]
        public bool ButtonDoAllRooms = false;
        public bool ButtonCreateExamples = false;
        public bool ButtonDestroyAllChildren = false;


        [Header("Enable Items")]
        
        [SerializeField]
        public ToggleTags ToggleTag = new ToggleTags();
        public bool ButtonToggleTagActive = false;

        [Header("Json Import/Export")]
        public bool ButtonJsonImport = false;
        public bool ButtonJsonExport = false;

        [Header("Room List")]
        public Cl_Floor floor = new Cl_Floor();    

        [Header("Materials")]
        public C_Materials materials;
        
        public int amountExampleRooms = 15;
        #endregion

        #region main
        // Start is called before the first frame update

        void init()
        {
            materials.init();
            floor = new Cl_Floor("1st Level",2.5f,materials);
        }
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
            if (ButtonDoAllRooms)
            {
                ButtonDoAllRooms = false;
                floor.create(gameObject);
            }

            if (ButtonToggleTagActive)
            {
                string toggleTag = "";
                switch (ToggleTag)
                {
                    case ToggleTags.ceiling: toggleTag = "ceiling"; break;
                    case ToggleTags.door: toggleTag = "door"; break;
                    case ToggleTags.window: toggleTag = "window"; break;
                }
                
                ButtonToggleTagActive = false;
                List<GameObject> found = Cl_MyMaster.findChildrenByTagMultiLevel(toggleTag, gameObject,5);
                Debug.Log("CALL ToggleTagActive(): "+toggleTag); 
                foreach (GameObject go in found)
                {
                    // Debug.Log("ToggleTagActive(): " + go.transform.parent.parent.name);
                    go.SetActive(!go.activeSelf);
                }
            }
            
            if (ButtonJsonImport)
            {
                ButtonJsonImport = false;
                floor.clear();
                json_import(jsonFile,jsonPath);
            }
            if (ButtonJsonExport)
            {
                ButtonJsonExport = false;
                json_export(jsonFile,jsonPath);
            }
            if(ButtonCreateExamples)
            {
                ButtonCreateExamples = false;
                floor.clear();
                init();                
                createExampleList();
            }
            if(ButtonDestroyAllChildren)
            {
                ButtonDestroyAllChildren = false;
                Cl_MyMaster.destroyAllChildren(gameObject);
            }
        }    
        #endregion


        #region Example
        public void createExampleList()
        {
            // initialize room object
            Cl_Room _room;

            // create floor (override existing one)
            floor = new Cl_Floor("Wohnung",2.5f,materials);
            floor.wallThickness = 0.15f;
            
            //create Flur
            _room = new Cl_Room("Flur_p1",new Vector2(0f,0f),1.75f,6.35f);
                _room.activeWalls[0]=false; 
                _room.activeWalls[1]=false;     
                _room.activeWalls[2]=false; 
                _room.activeWalls[3]=false;      

                floor.rooms.Add(_room);

            //create Wohnzimmer
            _room = new Cl_Room("Wohnzimmer",new Vector2(0f,0f),4.95f,4.0f);  
                // _room.addLight();
                _room.addWindow("N",-1.2f) ;
                _room.addWindow("N",0.2f) ;
                _room.addDoor("N",1.4f) ;
                _room.addDoor("E",-1.50f) ;
                
                _room.activeWalls[1]=false; 
                _room.place(floor,"Flur_p1","WS");         
                floor.rooms.Add(_room);
            //create WC
            _room = new Cl_Room("Küche",new Vector2(0f,0f),2.25f,6.7f);  
                _room.addDoor("N",-2.7f) ; 
                _room.addDoor("N",0f) ; 
                _room.addModule(new WallModule("W",ModuleType.Window,new Rect(-0.5f,0.6f,1f,0.8f)))  ; 
                _room.addModule(new WallModule("W",ModuleType.Window,new Rect( 0.5f,0.6f,1f,0.8f)))  ; 
                _room.place(floor,"Wohnzimmer","SW");         
                floor.rooms.Add(_room);       
            
            //create Balkon
            _room = new Cl_Room("Balkon",new Vector2(0f,0f),1.75f,4f);  
                _room.addModule(new WallModule("N",ModuleType.Hole,new Rect(0f,1f,4.25f,1.5f)))  ; 
                _room.activeWalls[1]=false;   
                _room.place(floor,"Wohnzimmer","NE");     
                

                floor.rooms.Add(_room);
            //create Arbeitszimmer
            _room = new Cl_Room("Arbeitszimmer",new Vector2(0f,0f),4.5f,2.2f);  
                _room.addDoor("S",0f) ; 
                _room.addWindow("N",0f) ;
                _room.place(floor,"Flur_p1","NW");     
                floor.rooms.Add(_room);
            //create Kinderzimmer
            _room = new Cl_Room("Kinderzimmer",new Vector2(0f,0f),4.5f,2.25f);  
                _room.addDoor("S",0f) ;
                _room.addWindow("N",0f) ;
                _room.place(floor,"Arbeitszimmer","ES");  
                floor.rooms.Add(_room);
             //create Schlafzimmer
            _room = new Cl_Room("Schlafzimmer",new Vector2(0f,0f),4.5f,3.5f);  
                _room.addDoor("S",0.8f) ; 
                _room.addWindow("N",-0.6f) ;
                _room.addWindow("N",0.6f) ;
                _room.place(floor,"Kinderzimmer","ES");     
                floor.rooms.Add(_room);
            //create Bad
            _room = new Cl_Room("Bad",new Vector2(0f,0f),2.75f,1.75f);  
                _room.addDoor("W",0f) ; 
                _room.place(floor,"Schlafzimmer","SE");     
                floor.rooms.Add(_room);
            //create Kammer
            _room = new Cl_Room("Kammer",new Vector2(0f,0f),1.25f,1.75f);  
                _room.addDoor("W",0f) ;  
                _room.place(floor,"Bad","SE");     
                floor.rooms.Add(_room);
            //create Flur
            _room = new Cl_Room("Flur_p2",new Vector2(0f,0f),2.25f,2.2f);
                _room.addDoor("S",0f) ;
                _room.activeWalls[0]=false;
                // _room.addModule(new WallModule("N",ModuleType.Hole,new Rect(-0.80f,0f,1.4f,2.50f)))  ;     
                _room.activeWalls[2]=false;
                _room.activeWalls[3]=false;   
                _room.place(floor,"Kammer","WS");                
                floor.rooms.Add(_room);  
            // create WC
            _room = new Cl_Room("Gaeste-WC",new Vector2(0f,0f),2.25f,1.15f); 
                _room.addDoor("N",0f) ; 
                _room.place(floor,"Flur_p2","WS"); 
                floor.rooms.Add(_room);

            // // set walls for all rooms
            // floor.setActiveWalls(4,false); // ceiling off
        }
        #endregion        

        #region JSON
        public void json_export(string _jsonFile="Floor.json",string _jsonPath="")
        {
            if (_jsonPath == "")
            {
                _jsonPath = Path.Combine("Streamingassets", "json");
            } 
            string jsonText = JsonUtility.ToJson(floor,true);
            System.IO.File.WriteAllText(Path.Combine(Application.dataPath,_jsonPath,_jsonFile), jsonText); 
        }
        public void json_import(string _jsonFile="Floor.json",string _jsonPath="")    
        {       
            if (_jsonPath == "")
            {
                _jsonPath = Path.Combine("Streamingassets", "json");
            } 
            // Debug.Log(Path.Combine(Application.streamingAssetsPath,_jsonPath,_jsonFile));
            string jsonText = System.IO.File.ReadAllText(Path.Combine(Application.dataPath,_jsonPath,_jsonFile));
            floor =  JsonUtility.FromJson<Cl_Floor>(jsonText);                
        }
        #endregion

        #endregion // end main class
    }
}