using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Vault;

public class UDSModel : MonoBehaviour
{
  [System.NonSerialized]
  public vdkPointCloud udModel = new vdkPointCloud();
  [System.NonSerialized]
  public bool isLoaded = false;
  [System.NonSerialized]
  public Matrix4x4 pivotTranslation;
  [System.NonSerialized]
  public Matrix4x4 modelScale;
  [System.NonSerialized]
  public double scaledRange;
  [System.NonSerialized]
  public double[] centreLocation;
  [System.NonSerialized]
  public double[] baseOffset;

  vdkPointCloudHeader UDSHeader = new vdkPointCloudHeader();

  public bool geoLocate = false; //determines if the model should be located in the position in real space
  public string path = "";

  public string Path {
    get { return path; }
    set
    {
      path = value;
      if (isLoaded == true)
        udModel.Unload();

      isLoaded = false;
        
     }
  }

  void Start()
  {
  }

  // This gets called by VDKPPES if it isn't loaded already
  public void LoadModel()
  {
    if (!GlobalVDKContext.isCreated || isLoaded || Path == "" ||Path ==null)
      return;

    try
    {
      udModel.Load(GlobalVDKContext.vContext, Path, ref UDSHeader);
      pivotTranslation = Matrix4x4.Translate(new Vector3((float)UDSHeader.pivot[0], (float)UDSHeader.pivot[1], (float)UDSHeader.pivot[2]) );
      modelScale = Matrix4x4.Scale(new Vector3( (float)UDSHeader.scaledRange, (float)UDSHeader.scaledRange, (float)UDSHeader.scaledRange) );
      scaledRange= UDSHeader.scaledRange;
      centreLocation=UDSHeader.boundingBoxCenter;
      baseOffset=UDSHeader.baseOffset;
      
      isLoaded = true;
    }
    catch(System.Exception e)
    {
      Debug.LogError("Could not open UDS: " + Path+" "+ e.Message);
    }
  }
}
