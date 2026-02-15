using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode] 
public class MeshCompiner_ExecuteAll : MonoBehaviour
{
    public bool Execute = false;
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
            MeshCombiner[] allMeshCombiner = GetMeshMeshCombinerFromChildren();

            foreach (MeshCombiner combiner in allMeshCombiner)
            {
                combiner.Execute = true;
                // combiner.enabled = false;
            }
        }
    }

    public MeshCombiner[] GetMeshMeshCombinerFromChildren()
    {
        MeshCombiner[] allMeshCombiner = FindObjectsOfType<MeshCombiner>();
        
        Debug.Log("GetMeshMeshCombinerFromChildren(): length = " + allMeshCombiner.Length);

        return (allMeshCombiner);
        // List<MeshFilter> filteredMeshFilters = new List<MeshFilter>();

        // for (int i = 0; i < allMeshFilters.Length; i++)
        // {
        // 	// filter the parents meshfilter from array, so that it won't be deleted later
        // 	if (allMeshFilters[i].gameObject == ParentGO)
        // 	{
        // 		continue;
        // 	}
        // 	// filter methfilter if its tag is not in list
        // 	if (!FilterTags.Contains(allMeshFilters[i].gameObject.tag))
        // 	{
        // 		continue;
        // 	}
        // 	filteredMeshFilters.Add(allMeshFilters[i]);
        // }
        // return filteredMeshFilters.ToArray();
    }
}
