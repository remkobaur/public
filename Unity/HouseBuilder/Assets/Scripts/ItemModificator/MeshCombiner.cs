// code originally from 
// REF: https://github.com/kurtdekker/makegeo/blob/master/makegeo/Assets/CombineMeshes/ExampleFromUnityImproved/ExampleCombinerImproved.cs
//
﻿// code originally from this Unity3D website:
// https://docs.unity3d.com/ScriptReference/Mesh.CombineMeshes.html
//
// Improved by Kurt Dekker @kurtdekker
// 
// Usage:
// - make a blank object
// - put this script on it
// - parent all other mesh GameObjects below this one
// - run
// - voila!

using UnityEngine;
using System.Collections;
using System.Collections.Generic;

[RequireComponent(typeof(MeshFilter))]
[RequireComponent(typeof(MeshRenderer))]
[ExecuteInEditMode]  // Remko: EditorMode
public class MeshCombiner : MonoBehaviour
{
	[Header("Actions")]
	public bool Execute = false;  // Remko: Add "button"
	[Header("Settings")]
	[SerializeField]
	public List<string> FilterTags = new List<string>();
	public GameObject ParentGO = null;
	public bool destroyChildren = true;
	public bool attachRemainingSubChildren = false;
	public bool removeEmpty = false;

	private Vector3 org_pos = Vector3.zero;

	void Start()
	{

	}
	void Update()
	{
		if (Execute)
		{
			Execute = false;

			// move gameObject to origin and save original position
			org_pos = transform.position;
			transform.position = Vector3.zero;

			// set this GO as target for meshes and collider, if no ither parrent is passed
			if (ParentGO == null)
			{
				ParentGO = gameObject;
			}

			// process all children: 
			// Debug.Log("MeshCombiner:: Process parent <" + ParentGO.name + ">");
			CombineMeshes(); // merge meshes
			CombineColliders(); // merge collides
			removeChildren(); // remove children, which have been already merged
			attach_RemainingSubChildren();

			// remove left over empty GO trees (execute twice is required)
			removeEmptyChildren(transform);
			removeEmptyChildren(transform);

			// reset object position
			transform.position = org_pos;
			// deactivate this script after execution 
			GetComponent<MeshCombiner>().enabled = false;

			// DestroyImmediate(GetComponent<MeshCombiner>());
		}
	}


	public void removeEmptyChildren(Transform _parent)
	{
		if (removeEmpty)
		{
			// Debug.Log("check for remove empty go: "+_parent.name);
			foreach (Transform child in _parent)
			{
				if (child.gameObject == ParentGO)
				{
					continue;
				}
				removeEmptyChildren(child);
			}

			Component[] components = _parent.gameObject.GetComponents(typeof(Component));
			// Debug.Log("check for remove empty go: " + _parent.name + "   components= "+components.Length+"   children= "+_parent.childCount );
			if (_parent.childCount == 0 && components.Length == 1)
			{
				// Debug.Log("remove empty child: " + _parent.name);
				_parent.parent = null;
				DestroyImmediate(_parent.gameObject);
			}
		}
	}

	public void attach_RemainingSubChildren()
	{
		if (attachRemainingSubChildren)
		{
			MeshFilter[] meshFilters = GetComponentsInChildren<MeshFilter>();
			for (int i = 0; i < meshFilters.Length; i++)
			{
				meshFilters[i].transform.parent = transform;
			}
		}
	}

	public void removeChildren()
	{
		MeshFilter[] meshFilters = GetMeshfiltersFromChildren();
		// deactivate children
		for (int i = 0; i < meshFilters.Length; i++)
		{
			if (FilterTags.Contains(meshFilters[i].gameObject.tag))
			{

				// if (meshFilters[i].gameObject == ParentGO)
				// {
				// 	continue;
				// }

				if (!destroyChildren)
				{
					// Debug.Log("deactivate child: " + meshFilters[i].gameObject.name);
					meshFilters[i].gameObject.SetActive(false);
				}
				else
				{
#if UNITY_EDITOR
					UnityEngine.Object.DestroyImmediate(meshFilters[i].gameObject);
#else
					UnityEngine.Object.Destroy(meshFilters[i].gameObject);
#endif
				}
			}
		}
	}
	public void CombineColliders()
	{
		MeshFilter[] meshFilters =GetMeshfiltersFromChildren();
		// copy colliders
		for (int i = 0; i < meshFilters.Length; i++)
		{
			// if (!FilterTags.Contains(meshFilters[i].gameObject.tag))
			// {
			// 	continue;
			// }
			if (meshFilters[i].gameObject.TryGetComponent<BoxCollider>(out BoxCollider colli))
			{
				// Debug.Log("Scale" + meshFilters[i].transform.localScale);
				//get transformed scale
				Vector3 worldScale = Vector3.Scale(meshFilters[i].transform.localScale, transform.localScale);
				worldScale = meshFilters[i].transform.TransformDirection(worldScale);
				worldScale = new Vector3(Mathf.Abs(worldScale.x), Mathf.Abs(worldScale.y), Mathf.Abs(worldScale.z));

				//get transformed position
				Vector3 worldPos = meshFilters[i].transform.position;

				//create collider comonent
				BoxCollider bc = ParentGO.AddComponent<BoxCollider>();
				bc.size = worldScale;
				bc.center = worldPos;
			}
		}
	}
	public void CombineMeshes() // Remko: moved code from start() to this button triggered method
	{
		//add Meshfilter to Parent if missing
		if (!ParentGO.transform.TryGetComponent<MeshFilter>(out MeshFilter meshFilter))
		{
			ParentGO.AddComponent<MeshFilter>();
		}
		//add MeshRenderer to Parent if missing
		if (!ParentGO.transform.TryGetComponent<MeshRenderer>(out MeshRenderer meshRenderer))
		{
			ParentGO.AddComponent<MeshRenderer>();
		}
		// get meshfilters of all children
		MeshFilter[] meshFilters = GetMeshfiltersFromChildren();
		List<CombineInstance> combines = new List<CombineInstance>();

		// KurtFixed: handle materials... I mean, they're kind of important!
		List<Material> materials = new List<Material>();

		for (int i = 0; i < meshFilters.Length; i++)
		{
			// KurtFixed: we gotta ignore ourselves or our count would be off!
			// if (meshFilters[i] == GetComponent<MeshFilter>())
			// {
			// 	continue;
			// }
			// if (!FilterTags.Contains(meshFilters[i].gameObject.tag))
			// {
			// 	continue;
			// }
			// KurtFixed: tally up the materials, since each mesh could have multiple
			var mr = meshFilters[i].GetComponent<MeshRenderer>();
			for (int j = 0; j < mr.sharedMaterials.Length; j++)
			{
				var combine = new CombineInstance();

				combine.mesh = meshFilters[i].sharedMesh;
				combine.subMeshIndex = j;

				combine.transform = meshFilters[i].transform.localToWorldMatrix;
				// combine.transform.position -= mr.transform.parent.position;			

				combines.Add(combine);
				materials.Add(mr.sharedMaterials[j]);
			}
		}
		ParentGO.transform.GetComponent<MeshFilter>().sharedMesh = new Mesh();
		ParentGO.transform.GetComponent<MeshFilter>().sharedMesh.CombineMeshes(combines.ToArray(), false);

		// KurtFixed: inject the original materials
		ParentGO.GetComponent<MeshRenderer>().materials = materials.ToArray();
	}
	
	public MeshFilter[] GetMeshfiltersFromChildren()
	{
		MeshFilter[] allMeshFilters = GetComponentsInChildren<MeshFilter>();
		List<MeshFilter> filteredMeshFilters = new List<MeshFilter>();

		for (int i = 0; i < allMeshFilters.Length; i++)
		{
			// filter the parents meshfilter from array, so that it won't be deleted later
			if (allMeshFilters[i].gameObject == ParentGO)
			{
				continue;
			}
			// filter methfilter if its tag is not in list
			if (!FilterTags.Contains(allMeshFilters[i].gameObject.tag))
			{
				continue;
			}
			filteredMeshFilters.Add(allMeshFilters[i]);
		}
		return filteredMeshFilters.ToArray();
	}
}
