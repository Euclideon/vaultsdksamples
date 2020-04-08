from os.path import abspath
from PIL import Image

import vault
SDKPath=''
vault.LoadVaultSDK(SDKPath)
modelFile = abspath("../../samplefiles/DirCube.uds")
class VDKEasyRenderer():
  def __init__(self,
               userName, password, serverPath="https://earth.vault.euclideon.com",
               width=1280, height=720, clearColour=0,
               models=[modelFile]
               ):
    self.vaultContext = vault.vdkContext()
    self.vaultRenderer = vault.vdkRenderContext()
    self.log_in(userName, password, serverPath)

    self.vaultModels = []
    for model in models:
      self.add_model(model)

    self.renderViews = []
    self.add_view()

  def add_model(self, fileName):
    """
    Parameters
    ----------
    fileName: the path to UDS file to be added to the render list
    """
    model = vault.vdkPointCloud()
    try:
      model.Load(self.vaultContext, fileName)
    except vault.VdkException as e:
      print("Load model {} failed: {}".format(fileName, e.args[1]))
      return
    self.vaultModels.append(model)

  def log_in(self, userName: str, userPass: str, serverPath: str) -> None:
    appName = "Python Sample"
    print('Logging in to vault server...')
    self.vaultContext.Connect(serverPath, appName, userName, userPass)
    self.vaultContext.RequestLicense(vault.vdkLicenseType.Render)
    self.vaultRenderer.Create(self.vaultContext)
    print('Logged in')

  def add_view(self,x=0, y=-5, z=0, roll=0, pitch=0, yaw=0):
    view = vault.vdkRenderView(context=self.vaultContext, renderContext=self.vaultRenderer)
    view.set_view(x, y, z, roll, pitch, yaw)
    self.renderViews.append(view)
    return view

  def main_view(self):
    return self.renderViews[0]

  def render_view(self, view):
    self.vaultRenderer.Render(view, self.vaultModels)

  def render_all(self):
    for view in self.renderViews:
      self.vaultRenderer.Render(view, self.vaultModels)

  def render_to_file(self, outFile: str):
    for x in range(10):
      self.render_all()
    i=0
    for view in self.renderViews:
      name = outFile + '_'+str(i)+'.png'
      Image.frombuffer("RGBA", (view.width, view.height), view.colourBuffer, "raw", "RGBA", 0, 1).save(name)
      i += 1


  def __del__(self):
    for model in self.vaultModels:
      model.Unload()


if __name__ == "__main__":
  renderer = VDKEasyRenderer('bwockner','newVaultPassword')
  renderer.add_view(5,0,0,0,0,-3.14/2)
  renderer.add_view(0,5,0,0,0,3.14)
  renderer.add_view(-5,0,0,0,0,3.14/2)
  renderer.add_view(0,-5,5,-3.14/4,0,0)
  renderer.add_view(-5,0,5,0,-3.14/4,3.14/2)
  renderer.add_view(5,0,5,0,-3.14/4,-3.14/2)
  renderer.add_view(0,5,5,-3.14/4,0,3.14)
  renderer.render_to_file("testIm")
