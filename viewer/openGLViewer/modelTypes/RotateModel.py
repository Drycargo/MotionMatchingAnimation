from viewer.openGLViewer.GeometryModel import GeometryModel
import glm

class RotateModel(GeometryModel):
    def __init__(self, renderEngine, vertexArrayName, axis, rotationSpeed, textureName = None):
        super(RotateModel, self).__init__(renderEngine, vertexArrayName, textureName)
        self.rotationAxis = axis
        self.rotationSpeed = rotationSpeed

    def updateMatrices(self):
        #Overwrite
        self.modelMat = glm.rotate(self.modelMat, self.rotationSpeed, self.rotationAxis)