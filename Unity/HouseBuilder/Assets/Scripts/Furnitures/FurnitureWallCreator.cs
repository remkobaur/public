using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
namespace My.ns_Furniture
{

    [ExecuteInEditMode]
    public class FurnitureWallCreator : MonoBehaviour
    {
        [Header("ACTIONS")]
        public bool ButtonCreateAllFurnitures = false;
        // public bool ButtonCreateExamples = false; 
        public bool ButtonDestroyAllChildren = false;

        private bool ButtonCreateExampleList = false;

        [Header("Settings")]
        public bool enableMergeMeshes = true;
        public Vector3 handleOffset = new Vector3(0.02f,0.07f,0.005f);
        [SerializeField]
        List<Cl_Furniture> furnitureList = new List<Cl_Furniture>();

        public bool copyLastFurniture = false;
        public Material material;

        [Header("Prefabs")]
        public GameObject handle = null;
        public GameObject front = null;

        // Start is called before the first frame update
        void Start()
        {

        }

        // Update is called once per frame
        void Update()
        {
            if (ButtonCreateExampleList)
            {
                ButtonCreateExampleList = false;
                create_example_list();
            }
            if (copyLastFurniture)
            {
                copyLastFurniture = false;
                furnitureList.Add(furnitureList.Last());
            }

            if (ButtonCreateAllFurnitures)
            {
                ButtonCreateAllFurnitures = false;
                GameObject FurnCluster = new GameObject("FurnitureCluster");
                FurnCluster.transform.parent = transform;
                FurnCluster.transform.localPosition = Vector3.zero;

                float offset = 0.0f;
                foreach (Cl_Furniture furniture in furnitureList)
                {

                    // Debug.Log("FurnitureWallCreator: Create <" + furniture.name + ">");
                    // furniture.enableMergeMeshes = enableMergeMeshes;
                    furniture.material = material;
                    furniture.handleOffset = handleOffset;
                    furniture.construct_shelf();
                    FurnitureCreator FC = FurnCluster.AddComponent<FurnitureCreator>();
                    FC.enableMergeMeshes = enableMergeMeshes;
                    furniture.material = material;
                    FC.furniture = furniture;
                    FC.handle = handle;
                    FC.front = front;
                    FC.material = material;
                    FC.furnGO = new GameObject(furniture.name);
                    FC.furnGO.transform.parent = FurnCluster.transform;
                    FC.ButtonCreateShelf = true;
                    if (FC.furnGO != null)
                    {
                        offset += furniture.width / 2.0f+furniture.posOffset.z;
                        // if (furniture.posOffset.y != 0.0f)
                        // {
                        //    FC.furnGO.transform.localPosition = new Vector3(furniture.posOffset.x, furniture.posOffset.y +furniture.height / 2.0f, offset);
                        // }
                        // else
                        // {
                        //     FC.furnGO.transform.localPosition = new Vector3(furniture.posOffset.x, furniture.posOffset.y, offset);
                        // }
                        FC.furnGO.transform.localPosition = new Vector3(furniture.posOffset.x, furniture.posOffset.y, offset);
                        
                        
                        offset += furniture.width / 2.0f;
                    }
                    else
                    {
                        Debug.LogWarning("FC.furnGO is null for Furniture:  " + furniture.name);
                    }
                }
                FurnCluster.transform.rotation = transform.rotation;
            }
            // if(ButtonCreateExamples)
            // {
            //     ButtonCreateExamples = false;                
            //     init_furniture();
            // }

            if (ButtonDestroyAllChildren)
            {
                ButtonDestroyAllChildren = false;
                Cl_MyMaster.destroyAllChildren(gameObject);
            }

        }

        public void create_example_list()
        {
            furnitureList.Clear();

            for (int i = 1; i <= 3; i++)
            {
                Cl_Furniture furniture = new Cl_Furniture();
                furniture.name = "CubBoard" + (i);
                furniture.height = 0.7f;
                furniture.width = 0.4f;
                furniture.depth = 0.4f;
                furniture.thickBoard = 0.015f;
                furniture.thickFrame = 0.015f;
                furniture.rows = 3;
                furniture.cols = 1;
                // furniture.footbar = 0.0f;
                furniture.enableMergeMeshes = enableMergeMeshes;
                furniture.handleOffset = new Vector3(0.05f,0.1f,0f);
                furniture.doorType = e_doorType.left;
                furniture.material = material;
                furnitureList.Add(furniture);
            }
        }          
    }
}