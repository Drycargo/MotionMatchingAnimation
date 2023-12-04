from viewer.openGLViewer.ShaderPrograms import ShaderPrograms
from viewer.openGLViewer.VertexBuffer import VertexBufferManager

class VertexArrayManager:
    def __init__(self, context):
        self.context = context
        self.vertexArrays = {}
        self.shaderPrograms = ShaderPrograms(self.context)
        self.vertexBufferManager = VertexBufferManager(self.context)

        # Add Cube
        self.addVertexArray(vertArrayName = "Cube", shaderName = "default", bufferName = "Cube")
        # Add Reference Plane
        self.addVertexArray(vertArrayName = "RefPlane", shaderName = "refGrid", bufferName = "Plane")

    def getVertexArray(self, name):
        return self.vertexArrays[name]

    def addShader(self, fragShaderName, vertShaderName = None):
        return self.shaderPrograms.addShaderProgram(fragShaderName, vertexShaderName=vertShaderName)

    def addBuffer(self, name, dataIndPairs = [], \
                  config = {'format': '2f 3f 3f', 'attr': ['in_texcoord_0', 'in_normal', 'in_position']}):
        return self.vertexBufferManager.addVertexBuffer(name, dataIndPairs, config)

    def addVertexArray(self, vertArrayName, shaderName, bufferName):
        shader = self.shaderPrograms.getShaderProgram(shaderName)
        (buffer, vertFormat, attributes) = self.vertexBufferManager.getVertexBufferTuple(bufferName)

        newVertArray = self.context.vertex_array(
            shader,
            [(buffer, vertFormat, *attributes)]
        )
        self.vertexArrays[vertArrayName] = newVertArray

        return newVertArray

    def getVertexArray(self, name):
        return self.vertexArrays[name]

    def destroy(self):
        self.vertexBufferManager.destroy()
        self.shaderPrograms.destroy()

        for vertArray in self.vertexArrays.values():
            vertArray.release()