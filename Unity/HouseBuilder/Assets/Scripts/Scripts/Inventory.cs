using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using My.ns_Furniture;

[System.Serializable] 
public class InventoryItem
{
    public GameObject obj = null;
    public int slotID = 0;
    public Vector3 pos = Vector3.zero;

    // private Vector3 VZ = Vector3.zero; 
    public InventoryItem(GameObject _go,int _slotId, Vector3 _pos)
    {
        obj = _go;
        slotID = _slotId;
        pos = _pos;
    }
    
}

[ExecuteInEditMode]
#region Main Class
public class Inventory : MonoBehaviour
{    
    #region Parameters
    [Header("Create Example")]
    public string prefabPath="Prefabs/Items/Box_30cm";
    public int N_objects=10;
    public bool Exectue = false ;
    public bool ClearList = false;
    [Header("Dimensions")]

    public Cl_Furniture properties = new Cl_Furniture();

    [Header("Inventory")]
    public List<InventoryItem> inventory = new List<InventoryItem>();

    
    #endregion Parameters

    #region Main
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        buttonActions();
    }
    #endregion Main

    #region Button Actions
    public void buttonActions()
    {        
        if (Exectue)
        {
            Exectue = false;

            GameObject itemPrefab = Resources.Load(prefabPath) as GameObject;
            if (itemPrefab == null)
            {
                Debug.LogWarning($"Prefab <{prefabPath}> not found ");
            }

            for(int k=0;k<N_objects;k++)
            {
                spawnInventory(itemPrefab,k);
            }
        }
        if (ClearList)
        {
            ClearList = false;
            init();            
        }
        return;
    }
    public void init()
    {
        Cl_MyMaster.destroyAllChildren(gameObject);
        inventory = new List<InventoryItem>();
        properties = GetComponent<Furniture>().properties;
    }

    public void spawnInventory(GameObject _prefab,int _slotId)
    {
       GameObject _go = Instantiate(_prefab, new Vector3(0, 0, 0), Quaternion.identity);
       _go.transform.parent = transform;
       _go.transform.localPosition = get_slotOrigin(_slotId);
       _go.transform.localRotation =  Quaternion.identity;
       addItem(_go,_slotId,get_slotOrigin(_slotId));
    }

    #endregion Button Actions

    #region locations
    private Vector3 get_slotOrigin(int _slotID)
    {
        int slotID = _slotID;
        float width = properties.width-2f*properties.thickFrame;
        float height = properties.height-2f*properties.thickFrame-properties.footbarHeight;
        float dw = (width+properties.thickBoard)/(float)properties.cols;
        float dh = (height)/(float)properties.rows;
        float ofs_h = properties.footbarHeight+properties.thickFrame;
        float ofs_w = -width/2f+dw/2f-properties.thickBoard/2f ;
        Vector3 _pos = new Vector3(
            -properties.depth/2f,
            dh*(float)(slotID/properties.cols) + ofs_h,
            dw*(float)(slotID%properties.cols ) + ofs_w
        );
        return _pos;
    }
    #endregion

    #region add and remove Items
    public void addItem(GameObject _go,int _slotId,Vector3 _pos)
    {
        if(_go == null)
        {
            return;
        }      
        inventory.Add(new InventoryItem(_go,_slotId,_pos));
        _go.transform.parent = transform;
        _go.transform.localPosition = _pos;
    }

    public void removeItem(GameObject _go)
    {
        if(_go == null)
        {
            return;
        }
        foreach(InventoryItem item in inventory)
        {
            if (item.obj == _go)
            {
                inventory.Remove(item);
                _go.transform.parent = null; 
            }
        }
    }
    #endregion add and remove Items
}
#endregion Main Class
