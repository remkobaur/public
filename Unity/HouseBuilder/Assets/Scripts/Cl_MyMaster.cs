using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class Cl_MyMaster
{
    public static GameObject createChild(string _name, GameObject _parent)
    {
        GameObject go = new GameObject(_name);
        go.transform.parent = _parent.transform;
        go.transform.localPosition = Vector3.zero;
        //go.name = _name
        return go;
    }
    public static void destroyAllChildren(GameObject _parent = null)
    {
        for (int i = _parent.transform.childCount; i > 0; --i)
        {
            UnityEngine.Object.DestroyImmediate(_parent.transform.GetChild(0).gameObject);
            // UnityEngine.Object.Destroy(_parent.transform.GetChild(0).gameObject);
            // DestroyImmediate(_parent.transform.GetChild(0).gameObject);  
        }

    }
    public static List<GameObject> findChildrenByTag(string tag, GameObject _parent = null)
    {
        List<GameObject> found = new List<GameObject>();
        if (_parent == null)
        {
            return found;
        }

        foreach (Transform child in _parent.transform)
        {
            if (child.tag == tag)
                found.Add(child.gameObject);
        }
        return found;
    }
    
    public static List<GameObject> findChildrenByTagMultiLevel(string tag, GameObject _parent=null, int level = 0)
    {
        List<GameObject> found = new List<GameObject>();
        if (_parent==null)
        {
            return found;
        }

        foreach (Transform child in _parent.transform)
        {
            if (child.tag == tag)
                found.Add(child.gameObject);
            if (level > 0)
            {
                List<GameObject> subfound = findChildrenByTagMultiLevel(tag, child.gameObject, level-1);
                found.AddRange(subfound);
            }
        }
        return found;
    }

}

