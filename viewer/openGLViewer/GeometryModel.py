import glm
import numpy as np

from utils.Transform import ObjectTransform

class GeometryModel:
    def __init__(self, renderEngine, vertexArrayName, textureName = None, \
                 initPos = (0,0,0), initRot = (0,0,0), initScale = (1,1,1)):
        self.renderEngine = renderEngine
        self.transform = ObjectTransform(initPos, initRot, initScale)

        self.vertexArray = self.renderEngine.meshManager.vertArrayManager.getVertexArray(vertexArrayName)
        self.texture = self.renderEngine.meshManager.textureManager.getTexture(textureName) if textureName else None

        self.shaderProgram = self.vertexArray.program

        self.initialize()

    def initialize(self):
        self.shaderProgram['projectionMat'].write(self.renderEngine.camera.getProjectionMat())
        self.shaderProgram['viewMat'].write(self.renderEngine.camera.getViewMat())

        # Set Texture
        if self.texture:
            self.shaderProgram['u_texture_0'] = 0
            self.texture.use()

    def update(self):
        self.updateMatrices()
        self.setMatrices()
        self.setLight()
        self.shaderProgram['camWorldPos'].write(self.renderEngine.camera.position)

    def updateMatrices(self):
        self.modelMat = self.getModelMat()

    def setLight(self):
        for light in self.renderEngine.lights:
            self.shaderProgram['u_light.position'].write(light.position)
            self.shaderProgram['u_light.ambientI'].write(light.ambientI)
            self.shaderProgram['u_light.diffuseI'].write(light.diffuseI)
            self.shaderProgram['u_light.specularI'].write(light.specularI)

    def setMatrices(self):
        self.shaderProgram['viewMat'].write(self.renderEngine.camera.viewMat)
        self.shaderProgram['modelMat'].write(self.modelMat)

    def getModelMat(self):
        # Init
        modelMatrix = glm.mat4()

        # Translation
        modelMatrix = self.translateMatrix(modelMatrix)

        # Rotation
        modelMatrix = self.rotateMatrix(modelMatrix)

        # Scale
        modelMatrix = self.scaleMatrix(modelMatrix)
        return modelMatrix

    def scaleMatrix(self, modelMatrix):
        return glm.scale(modelMatrix, self.transform.scale)

    def rotateMatrix(self, modelMatrix):
        rotationRad = [np.radians(angleDeg) for angleDeg in self.transform.rotation]
        modelMatrix = glm.rotate(modelMatrix, rotationRad[0], glm.vec3(1,0,0))
        modelMatrix = glm.rotate(modelMatrix, rotationRad[1], glm.vec3(0,1,0))
        modelMatrix = glm.rotate(modelMatrix, rotationRad[2], glm.vec3(0,0,1))
        return modelMatrix

    def translateMatrix(self, modelMatrix):
        return glm.translate(modelMatrix, self.transform.position)

    def render(self):
        self.update()
        self.vertexArray.render()