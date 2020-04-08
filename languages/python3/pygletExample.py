import math

import vault
from easyrenderer import VDKEasyRenderer
import pyglet.window.key as keyboard
import pyglet
from camera import Camera
from os.path import abspath



class VDKViewPort():
  """This class represents the quad that the UDS render is blitted to,
  it handles the camera information associated with the view it controls
  """
  def __init__(self, width, height, centreX, centreY, parent):
    self._width = width
    self._height = height
    self._centreX = centreX
    self._centreY = centreY

    self.parent = parent

    self._view = parent.renderer.add_view()
    self._view.set_size(width, height)
    self.centreX = centreX
    self.centreY = centreY

    self._vertex_list = self.make_vertex_list()
    self._camera = Camera(self._view)
    self.im = pyglet.image.load('tmp.png')
    self.tex = self.im.get_texture()

  def make_vertex_list(self):
    return pyglet.graphics.vertex_list(4,
      # these are the vertices at the corners of the quad, each line is the pixel coordinates of the
      ('v2f', (  # vertices are represented as 2 element floats
        0.5 * (2 * self.centreX - self._width), 0.5 * (2 * self.centreY - self._height),
        0.5 * (2 * self.centreX + self._width), 0.5 * (2 * self.centreY - self._height),
        0.5 * (2 * self.centreX + self._width), 0.5 * (2 * self.centreY + self._height),
        0.5 * (2 * self.centreX - self._width), 0.5 * (2 * self.centreY + self._height),
      )),
      ('t2f', (  # texture coordinates as a float,
        0, 1,
        1, 1,
        1, 0,
        0, 0,
      )
       )
      )

  def render_uds(self, dt):
    from pyglet.gl import glEnable, GL_TEXTURE_2D, glDisable, glBindTexture

    self._camera.update_position(dt)
    #self._camera.look_at([0, 0, 0])
    self._camera.look_at()
    #self._camera.set_view(self._camera.cameraPosition[0],self._camera.cameraPosition[1],self._camera.cameraPosition[2],self._camera.camRotation[1],0,self._camera.camRotation[0])
    self.parent.renderer.render_view(self._view)
    #width, height = (self.renderWidth, (int) (self.renderWidth / self.texAR))
    self.im = pyglet.image.ImageData(self._width, self._height, 'RGBA', self._view.colourBuffer)
    self.tex = self.im.get_texture()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, self.tex.id)
    self._vertex_list.draw(pyglet.gl.GL_QUADS)
    glDisable(GL_TEXTURE_2D)

class VDKRenderCube(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        resolution = (900, 500)
        super(VDKRenderCube, self).__init__(*resolution)
        self.renderer = VDKEasyRenderer('username', 'password', models=[])

        self.renderer.add_model(abspath("../../samplefiles/DirCube.uds"))
        self.renderer.add_model("https://az.vault.euclideon.com/GoldCoast_20mm.uds")
        #self.renderer.add_model(abspath("../../samplefiles/Axis.uds"))
        self.viewPort = VDKViewPort(resolution[0]-100, resolution[1]-200, self._width//2, self._height//2, self)

        self.imageCounter = 0

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
      self.viewPort._camera.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_key_press(self, symbol, modifiers):
      if symbol == keyboard.W:
        self.viewPort._camera.forwardPressed = True
      if symbol == keyboard.S:
        self.viewPort._camera.backPressed = True
      if symbol == keyboard.D:
        self.viewPort._camera.rightPressed = True
      if symbol == keyboard.A:
        self.viewPort._camera.leftPressed = True
      if symbol == keyboard.E:
        self.viewPort._camera.upPressed = True
      if symbol == keyboard.C:
        self.viewPort._camera.downPressed = True
      if symbol == keyboard.LSHIFT:
        self.viewPort._camera.shiftPressed = True
      if symbol == keyboard.LCTRL:
        self.viewPort._camera.ctrlPressed = True


    def on_key_release(self, symbol, modifiers):
      if symbol == keyboard.W:
        self.viewPort._camera.forwardPressed = False
      if symbol == keyboard.S:
        self.viewPort._camera.backPressed = False
      if symbol == keyboard.D:
        self.viewPort._camera.rightPressed = False
      if symbol == keyboard.A:
        self.viewPort._camera.leftPressed = False
      if symbol == keyboard.E:
        self.viewPort._camera.upPressed = False
      if symbol == keyboard.C:
        self.viewPort._camera.downPressed = False
      if symbol == keyboard.LSHIFT:
        self.viewPort._camera.shiftPressed = False
      if symbol == keyboard.LCTRL:
        self.viewPort._camera.ctrlPressed = False

    #This was initially written to test blitting of images in files to textures
    def render_from_file(self, dt):
      from pyglet.gl import glEnable, GL_TEXTURE_2D, glDisable, glBindTexture
      self.im = pyglet.image.load('testIM_' + str(self.imageCounter) + '.png')
      self.tex = self.im.get_texture()
      glEnable(GL_TEXTURE_2D)
      glBindTexture(GL_TEXTURE_2D, self.tex.id)
      self.vertex_list.draw(pyglet.gl.GL_QUADS)
      glDisable(GL_TEXTURE_2D)
      self.imageCounter = (self.imageCounter + 1) % 7
    def on_draw(self):
      pass

    #def on_resize(self, width, height):
      #self.renderWidth = width - 100
      #renderHeight =(int) (self.renderWidth/self.texAR)
      #self.renderer.renderViews[0].set_size(self.renderWidth, renderHeight)

    def render_uds(self, dt):
      self.clear()
      fpsText = pyglet.text.Label("{} FPS".format((int)(1/dt)))
      fpsText.draw()

      positionTextWidth = 600
      positionText = pyglet.text.Label("x={:10.4f} y={:10.4f} z={:10.4f}\naxis = {} theta = {:10.4f}\n tangent ={}".format(*self.viewPort._camera.cameraPosition, self.viewPort._camera.rotationAxis, self.viewPort._camera.rotationTheta, self.viewPort._camera.tangentVector),multiline=True, width=positionTextWidth)
      positionText.y = self._height - 20
      positionText.x = self._width - positionTextWidth
      positionText.draw()

      self.viewPort.render_uds(dt)

    def on_close(self):
        self.__del__()
        pyglet.app.exit()

class VDKViewPort3D(VDKViewPort):
  """
  Viewport quad with 3D faces, used for constructing ViewPrisms
  """
  def __init__(self, width, height, centreX, centreY, parent):
    self._width = width
    self._height = height
    self._centre = [centreX, centreY, 0]
    self.parent = parent
    super(VDKViewPort3D, self)

  def orient(self, centre, vec1, vec2):
    #position the plane such that it is parallel to vectors 1 and 2 and centred at centre:
    # these are the vertices at the corners of the quad, each line is the pixel coordinates of the
    self.vertex_list.vertices = \
      [
        # bottom left
        centre[0] - vec1[0] * self._width / 2 - vec2[0] * self._height / 2,
        centre[1] - vec1[1] * self._width / 2 - vec2[1] * self._height / 2,
        centre[2] - vec1[2] * self._width / 2 - vec2[2] * self._height / 2,
        # bottom right
        centre[0] + vec1[0] * self._width / 2 - vec2[0] * self._height / 2,
        centre[1] + vec1[1] * self._width / 2 - vec2[1] * self._height / 2,
        centre[2] + vec1[2] * self._width / 2 - vec2[2] * self._height / 2,
        #top right
        centre[0] + vec1[0] * self._width/2 + vec2[0] * self._height/2,
        centre[1] + vec1[1] * self._width / 2 + vec2[1] * self._height / 2,
        centre[2] + vec1[2] * self._width / 2 + vec2[2] * self._height / 2,
        # top left
        centre[0] - vec1[0] * self._width / 2 + vec2[0] * self._height / 2,
        centre[1] - vec1[1] * self._width / 2 + vec2[1] * self._height / 2,
        centre[2] - vec1[2] * self._width / 2 + vec2[2] * self._height / 2,
      ]
    #position the camera such that it is a fixed distance from the
    import numpy as np
    v1 = np.array(vec1)
    v2 = np.array(vec2)

    normal = np.cross(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    self._camera.set_view(normal[0], normal[1], normal[2])

  def make_vertex_list(self):
    self.vertex_list = pyglet.graphics.vertex_list(4,'v3f/stream','t2f/static')
    self.vertex_list.tex_coords = \
      [
        0, 1,
        1, 1,
        1, 0,
        0, 0,
      ]
    self.orient(self.centre, self.vec1, self.vec2)


class VDKViewPrism:
  """
  Class representing a sectional view of a model
  it is a rectangular prism with a UD view for each face
  """
  def __init__(self, width, height, depth):
    self.height =height
    self.width = width
    self. depth = depth

    self.viewPorts = []

if __name__ == "__main__":
  cubeWindow = VDKRenderCube()
  pyglet.clock.schedule_interval(cubeWindow.render_uds, 1/60)
  pyglet.app.run()
  print('done')
