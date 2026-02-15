using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]  // Remko: EditorMode
public class ClusterCombiner : MonoBehaviour
{
    [Header("Actions")]
    public bool Execute = false;  // Remko: Add "button"

    [Header("Settings")]
    public string ClusterTag = "room";
    public List<string> MeshTags = new List<string>();
    public bool removeEmptyChildren = false;
    public bool attachRemainingSubChildren = true;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (Execute)
        {
            Execute = false;
            List<GameObject> ClusterGOs = Cl_MyMaster.findChildrenByTag(ClusterTag, gameObject);
            foreach (GameObject go in ClusterGOs)
            {
                MeshCombiner MC = go.AddComponent<MeshCombiner>();
                MC.FilterTags = MeshTags;
                MC.removeEmpty = removeEmptyChildren;
                MC.attachRemainingSubChildren = attachRemainingSubChildren;
                MC.enabled = true;
                MC.Execute = true;
                // DestroyImmediate(MC);
            }

        }
    }
}
