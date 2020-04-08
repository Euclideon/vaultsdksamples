import pyglet
from numpy.random import rand
import math
import pyglet.window.key as keyboard
import numpy as np
import vault

class Camera():
  def __init__(self, VDKview):
    self.moveSpeed = 0.1
    self.moveVelocity = [0, 0, 0]
    self.cameraPosition = [0, -5, 0]
    self.forwardPressed = False
    self.backPressed = False
    self.rightPressed = False
    self.leftPressed = False
    self.upPressed = False
    self.downPressed = False
    self.shiftPressed = False
    self._view = VDKview
    self.mouseSensitivity = 1 / 100
    self.camRotation = [0, 0, 0]
    self.lookAtTarget = [0, 0, 0]

    self.rotationMatrix = np.array([[1, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, 1]])
    self.matrix = np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])
    self.facingDirection = [0, 1, 0]
    self.rotationAxis = np.array([0,0,1])
    self.tangentVector = np.array([0,1,0])
    self.rotationTheta = 0

  def set_view(self, x=0, y=-5, z=0, roll=0, pitch=0,yaw=0):
    sy = math.sin(yaw)
    cy = math.cos(yaw)
    sp = math.sin(pitch)
    cp = math.cos(pitch)
    sr = math.sin(roll)
    cr = math.cos(roll)

    self.matrix = np.array([
      [cy*cp, cy*sp*sr-sy*cr, cy*sp*cr+sy*sr, 0],
      [sy*cp, sy*sp*sr+cy*cr, sy*sp*cr-cy*sr, 0],
      [-sp, cp*sr, cp*cr, 0],
      [x, y, z, 1]
    ])
    self.rotationMatrix = self.matrix[:3, :3]
    self._view.SetMatrix(vault.vdkRenderViewMatrix.Camera, self.matrix.flatten())

  def axisAngle(self,axis, theta):
    #cTheta = np.dot(np.array([0,1,0]), dPoint) / np.linalg.norm(dPoint)
    #theta = np.arccos(cTheta)
    cTheta = np.cos(theta)
    sTheta = np.sin(theta)

    self.matrix = np.array(
      [
        [cTheta + axis[0] ** 2 * (1 - cTheta), axis[0] * axis[1] * (1 - cTheta) - axis[2] * sTheta, axis[0] * axis[2] * (1 - cTheta), 0],
        [axis[1] * axis[0] * (1 - cTheta) + axis[2] * sTheta, cTheta + axis[1] ** 2 * (1 - cTheta), axis[1] * axis[2] * (1 - cTheta) - axis[0] * sTheta, 0],
        [axis[2] * axis[0] * (1 - cTheta) - axis[1] * sTheta, axis[2] * axis[1] * (1 - cTheta) + axis[0] * sTheta, cTheta + axis[2] ** 2 * (1 - cTheta), 0],
        [self.cameraPosition[0], self.cameraPosition[1], self.cameraPosition[2], 1]
      ]
    )

  def look_at(self, lookAtPoint=None, cameraPosition=None):
    """
    faces the camera at point2, positions the camera at point1
    Parameters
    ----------
    cameraPosition: position of the camera
    lookAtPoint: x, y, z tuple to face the camera towards
    """
    if cameraPosition is None:
      cameraPosition = self.cameraPosition
    else:
      self.cameraPosition = cameraPosition

    if lookAtPoint is None:
      lookAtPoint = self.lookAtTarget

    if not np.array_equal(lookAtPoint, cameraPosition):
      #calculate our axis of rotation based on the distance between these points
      dPoint = np.array(lookAtPoint) - np.array(cameraPosition)
    else:
      dPoint = np.array([1, 1, 0])

    tangent = [0, 0, 0]
    tangent[0] = (dPoint[0]-np.sqrt(dPoint[0]**2+4*dPoint[1]**2))/(2*dPoint[1])
    tangent[1] = 1-tangent[0]**2
    tangent = -np.array(tangent)
    tangent = tangent / np.sqrt(tangent.dot(tangent))

    forward = dPoint/np.sqrt(dPoint.dot(dPoint))
    axis = np.cross(tangent, forward)
    axis = axis / np.sqrt(axis.dot(axis))

    self.matrix = np.array(
      [
        [tangent[0], tangent[1], tangent[2], 0],
        [forward[0], forward[1], forward[2],0],
        [axis[0], axis[1], axis[2], 0],
        [cameraPosition[0], cameraPosition[1], cameraPosition[2], 1]
      ]
    )
    self.rotationAxis = axis
    self.tangentVector = tangent
    self.rotationMatrix = self.matrix[:3, :3]
    self._view.SetMatrix(vault.vdkRenderViewMatrix.Camera, self.matrix.flatten())

  def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    horiz = dx * self.tangentVector * self.mouseSensitivity
    vert = dy * self.rotationAxis * self.mouseSensitivity
    if not self.ctrlPressed:
      self.lookAtTarget = self.lookAtTarget + horiz + vert
    else:
      self.cameraPosition = self.cameraPosition - horiz - vert


  def update_move_direction(self):
    self.moveVelocity = [0, 0, 0]# in local coordinates
    if self.shiftPressed:
      self.moveSpeed = 1
    else:
      self.moveSpeed = 0.3
    if self.forwardPressed:
      self.moveVelocity[1] += self.moveSpeed
    if self.backPressed:
      self.moveVelocity[1] -= self.moveSpeed
    if self.rightPressed:
      self.moveVelocity[0] += self.moveSpeed
    if self.leftPressed:
      self.moveVelocity[0] -= self.moveSpeed
    if self.upPressed:
      self.moveVelocity[2] += self.moveSpeed
    if self.downPressed:
      self.moveVelocity[2] -= self.moveSpeed
    self.moveVelocity = np.array(self.moveVelocity).dot(self.rotationMatrix).tolist()

  def update_position(self, dt):
    self.update_move_direction()
    self.cameraPosition[0] = self.cameraPosition[0] + self.moveVelocity[0]*dt
    self.cameraPosition[1] = self.cameraPosition[1] + self.moveVelocity[1]*dt
    self.cameraPosition[2] = self.cameraPosition[2] + self.moveVelocity[2]*dt
