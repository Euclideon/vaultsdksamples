using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using Vault;

/*
 *Loads all uds files in a local path and places them in the world space relative to the first
 * Intended for multi part uds files
 */
public class loadAllUDSInDirectory : MonoBehaviour
{
    public string path;
    void Start()
    {
        string[] files = Directory.GetFiles(path);
        double[] rootBaseOffset = new double[3];
        int baseInd = 0; //index in the list to which all models will be placed relative to
        for (int i = 0; i < files.Length; ++i)
        {
            string file = files[i];
            //skip non uds files
            if (!file.Substring(file.Length - 4).Equals(".uds"))
            {
                if (i == baseInd)
                    ++baseInd;
                continue;
            }

            GameObject modelGameObject = new GameObject(file);
            modelGameObject.transform.SetParent(this.transform);
            modelGameObject.AddComponent<UDSModel>();
            UDSModel model = modelGameObject.GetComponent<UDSModel>();
            model.path = file;
            try
            {
                model.LoadModel();
                model.modelScale = Matrix4x4.identity;
            }
            catch
            {
                Debug.LogError("load model failed: " + file);
                if (i == baseInd)
                    ++baseInd;
                continue;
            }
            double[] baseOffset = model.header.baseOffset;
            
            if (i == baseInd)//reference all models to the first 
                rootBaseOffset = model.header.baseOffset;

            model.transform.localPosition =
                new Vector3
                (
                    (float)(baseOffset[0] - rootBaseOffset[0]),
                    (float)(baseOffset[1] - rootBaseOffset[1]),
                    (float)(baseOffset[2] - rootBaseOffset[2])
                );
            model.transform.localScale = new Vector3((float)model.header.scaledRange, (float)model.header.scaledRange, (float)model.header.scaledRange);
            //model.transform.localRotation = Quaternion.Euler(-90, 0, 0);
            modelGameObject.tag = "UDSModel";
        }
    }
}
