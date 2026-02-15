using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace My.ns_Furniture{
    [ExecuteInEditMode]
    public class SetMaterialForAllChilds : MonoBehaviour
    {
        public Material materialBoards=null;
        public Material materialDoor=null;
        public Material materialHandle=null;
        public bool Execute = false;
        // Start is called before the first frame update
        void Start()
        {
            
        }

        // Update is called once per frame
        void Update()
        {
            buttonActions();
        }
        public void buttonActions()
        {
            if (Execute)
            {
                Execute = false;
                if (materialBoards != null)
                {
                    //update all board childs
                    List<GameObject> boards = Cl_MyMaster.findChildrenByTag("board", gameObject);
                    foreach (GameObject go in boards)
                    {
                        go.GetComponent<MeshRenderer>().material = materialBoards;
                    }

                    //update all materials in meshrender 
                    MeshRenderer MR = gameObject.GetComponent<MeshRenderer>();

                    if (MR != null)
                    {
                        var materials = MR.sharedMaterials;
                        // Debug.Log("MR.sharedMaterials.Length = " + MR.sharedMaterials.Length);
                        for (int j = 0; j < materials.Length; j++)
                        {                            
                            materials[j] = materialBoards;
                        }
                        MR.sharedMaterials = materials;
                    }
                }
                //update doors
                
                List<GameObject> doors = Cl_MyMaster.findChildrenByTag("door", gameObject);
                foreach (GameObject go in doors)
                {
                    if (materialDoor != null)
                    {
                        go.GetComponent<MeshRenderer>().material = materialDoor;
                    }
                    if (materialHandle != null)
                    { 
                        List < GameObject > handles = Cl_MyMaster.findChildrenByTag("handle", go);
                        foreach (GameObject handle in handles)
                        {
                            //update all materials in meshrender 
                            MeshRenderer MR = handle.GetComponent<MeshRenderer>();
                            if (MR != null)
                            {
                                var materials = MR.sharedMaterials;
                                // Debug.Log("MR.sharedMaterials.Length = " + MR.sharedMaterials.Length);
                                for (int j = 0; j < materials.Length; j++)
                                {
                                    Debug.Log("set material <" + materials[j].name + "> of handle <" + handle.name + "> to " + materialHandle.name);
                                    materials[j] = materialHandle;
                                }
                                MR.sharedMaterials = materials;
                            }
                        }
                    }
                }               
            }
        }
    }
}