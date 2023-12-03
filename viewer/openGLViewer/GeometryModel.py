import glm

class GeometryModel:
    def __init__(self, renderEngine, vertexArrayName, textureName = None):
        self.renderEngine = renderEngine

        self.vertexArray = self.renderEngine.meshManager.vertArrayManager.getVertexArray(vertexArrayName)
        self.texture = self.renderEngine.meshManager.textureManager.getTexture(textureName) if textureName else None

        self.shaderProgram = self.vertexArray.program
        self.modelMat = self.getModelMat()

        self.initialize()

    def initialize(self):
        self.shaderProgram['projectionMat'].write(self.renderEngine.camera.getProjectionMat())
        self.shaderProgram['viewMat'].write(self.renderEngine.camera.getViewMat())
        self.shaderProgram['modelMat'].write(self.modelMat)

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
        modelMatrix = glm.mat4()
        return modelMatrix

    def render(self):
        self.update()
        self.vertexArray.render()