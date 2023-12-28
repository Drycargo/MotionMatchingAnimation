import glm
import pygame as pg

FOV_DEG_DEFAULT = 50
NEAR_DEFAULT = 0.1
FAR_DEFAULT = 100

ROTATE_SENSITIVITY = 0.1
TRANSLATE_SENSITIVITY = 0.2#0.005
ZOOM_SENSITIVITY = 20

class Camera:
    def __init__(self, renderEngine, fovDeg = FOV_DEG_DEFAULT, near = NEAR_DEFAULT, far = FAR_DEFAULT, \
                 pos = glm.vec3(0), yaw = -90, pitch = 0):
        self.FOV_DEG = fovDeg
        self.NEAR = near
        self.FAR = far
        self.position = pos

        self.yaw = yaw
        self.pitch = glm.clamp(pitch, -89, 89)

        # Update rotation
        self.updateDirRotation()

        self.renderEngine = renderEngine
        self.aspectRatio = renderEngine.WINDOW_DIM[0] / renderEngine.WINDOW_DIM[1]
        self.viewMat = None
        self.update()

    def update(self):
        self.checkRotate()
        self.updateDirRotation()
        self.viewMat = self.getViewMat()

    def checkRotate(self):
        (dX, dY) = pg.mouse.get_rel()

        if self.renderEngine.mouseState.leftDown and not self.renderEngine.mouseState.operatingUi:
            self.yaw -= dX * ROTATE_SENSITIVITY
            self.pitch = glm.clamp(self.pitch + dY* ROTATE_SENSITIVITY, -89, 89)
        if self.renderEngine.mouseState.midDown:
            self.position -= TRANSLATE_SENSITIVITY * (self.rightDir * dX - self.upDir * dY)
        if self.renderEngine.mouseState.relScroll != 0:
            self.position += ZOOM_SENSITIVITY * self.forwardDir * self.renderEngine.mouseState.relScroll

    def updateDirRotation(self):
        yawRad = glm.radians(self.yaw)
        pitchRad = glm.radians(self.pitch)

        self.forwardDir = glm.normalize(
            glm.vec3(
                glm.cos(yawRad) * glm.cos(pitchRad),
                glm.sin(pitchRad),
                glm.sin(yawRad) * glm.cos(pitchRad)))

        self.rightDir = glm.normalize(glm.cross(self.forwardDir, glm.vec3(0, 1, 0)))
        self.upDir = glm.normalize(glm.cross(self.rightDir, self.forwardDir))

    def getProjectionMat(self):
        return glm.perspective(glm.radians(self.FOV_DEG), self.aspectRatio, self.NEAR, self.FAR)

    def getViewMat(self):
        return glm.lookAt(self.position, self.position + self.forwardDir, self.upDir)