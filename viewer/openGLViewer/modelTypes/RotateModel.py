from viewer.openGLViewer.GeometryModel import GeometryModel
import glm

class RotateModel(GeometryModel):
    def __init__(self, renderEngine, vertexArrayName, axis, rotationSpeed, textureName = None, \
                 initPos = (0,0,0), initRot = (0,0,0), initScale = (1,1,1)):
        super(RotateModel, self).__init__(renderEngine, vertexArrayName, textureName, initPos, initRot, initScale)
        self.rotationAxis = axis
        self.rotationSpeed = rotationSpeed

    def rotateMatrix(self, modelMatrix):
        return glm.rotate(self.modelMat, self.rotationSpeed, self.rotationAxis)
