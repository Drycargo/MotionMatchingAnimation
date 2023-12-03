from viewer.openGLViewer.GeometryModel import GeometryModel
import glm

class RotateModel(GeometryModel):
    def __init__(self, renderEngine, dataIndPairs, axis, rotationSpeed = 0, shaderDir = '\\shaders\\default'):
        super(RotateModel, self).__init__(renderEngine, dataIndPairs, shaderDir)
        self.rotationAxis = axis
        self.rotationSpeed = rotationSpeed

    def updateMatrices(self):
        #Overwrite
        self.modelMat = glm.rotate(self.modelMat, self.rotationSpeed, self.rotationAxis)