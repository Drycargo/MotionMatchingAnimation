import numpy as np
import glm
import pygame as pg
import re
from viewer.openGLViewer.VertexBuffer import VertexBufferObj

class GeometryModel:
    def __init__(self, renderEngine, dataIndPairs, shaderDir = '\\shaders\\default'):
        self.renderEngine = renderEngine
        self.rawVertexData = []

        #self.setVertexData(dataIndPairs)
        #self.vertexBuffer = self.getVertexBuffer()
        self.vertexBufferObj = VertexBufferObj(self.renderEngine.context, rawData=dataIndPairs, \
                                               config = {'format': '2f 3f 3f', 'attr': ['in_texcoord_0', 'in_normal', 'in_position']})

        self.shaderProgram = self.renderEngine.shaderManager.getShaderProgram('default')
        #self.shaderProgram = self.loadShader(self.getFileDirectory() + shaderDir)
        self.vertexArray = self.getVertexArray()
        self.modelMat = self.getModelMat()
        self.texture = None

        self.shaderProgram['projectionMat'].write(self.renderEngine.camera.getProjectionMat())
        self.shaderProgram['viewMat'].write(self.renderEngine.camera.getViewMat())
        self.shaderProgram['modelMat'].write(self.getModelMat())

    def getFileDirectory(self):
        return '\\'.join(re.split('\\\\|/', __file__)[:-1])

    def addTexture(self, texturePath):
        rawTexture = pg.image.load(self.getFileDirectory() + texturePath).convert()
        self.texture = self.renderEngine.context.texture(
            size = rawTexture.get_size(),
            components = 3,
            data = pg.image.tostring(rawTexture, 'RGB')
        )

        self.shaderProgram['u_texture_0'] = 0
        self.texture.use()

    def update(self):
        self.updateMatrices()
        self.setMatrices()
        self.setLight()

    def updateMatrices(self):
        self.modelMat = self.getModelMat()

    def setLight(self):
        for light in self.renderEngine.lights:
            self.shaderProgram['u_light.position'].write(light.position)
            self.shaderProgram['u_light.ambientI'].write(light.ambientI)
            self.shaderProgram['u_light.diffuseI'].write(light.diffuseI)
            self.shaderProgram['u_light.specularI'].write(light.specularI)
        self.shaderProgram['camWorldPos'].write(self.renderEngine.camera.position)

    def setMatrices(self):
        self.shaderProgram['viewMat'].write(self.renderEngine.camera.viewMat)
        self.shaderProgram['modelMat'].write(self.modelMat)

    def getModelMat(self):
        modelMatrix = glm.mat4()
        return modelMatrix

    def setVertexData(self, dataIndexPairs):
        self.rawVertexData = []

        # Triangles from each data-index pair must have the same order
        triangleCount = len(dataIndexPairs[0][1])
        propertyDimension = len(dataIndexPairs)

        # For each triangle:
        for triangleId in range(0, triangleCount):
            # For each triangle vertex:
            for vertexIdRaw in range(0, 3):
                # For each property corresponding to that vertex:
                resultProperties = ()
                for propertyId in range(0, propertyDimension):
                    vertexId = dataIndexPairs[propertyId][1][triangleId][vertexIdRaw]
                    resultProperties += dataIndexPairs[propertyId][0][vertexId]
                self.rawVertexData.append(resultProperties)
        '''
        for dataIndexPair in dataIndexPairs:
            for triangle in dataIndexPair[1]:
                for vertexId in triangle:
                    result = ()
                    for dataTuple in verticeDataGroups[vertexId]:
                        print(verticeDataGroups[vertexId])
                        result += dataTuple
                    self.rawVertexData.append(result)
        '''

    def getRawVertexData(self):
        return self.rawVertexData

    def getVertexBuffer(self):
        vertexData = np.array(self.getRawVertexData(), dtype="f4")
        return self.renderEngine.context.buffer(vertexData)

    def getVertexArray(self):
        return self.renderEngine.context.vertex_array(
            self.shaderProgram,
            [(self.vertexBufferObj.bufferObject,
              self.vertexBufferObj.vertDataFormat,
              *self.vertexBufferObj.vertDataAttr)])

    def loadShader(self, shaderDir):
        with open('{}.vert'.format(shaderDir)) as vertS:
            vertexShader = vertS.read()

        with open('{}.frag'.format(shaderDir)) as fragS:
            fragmentShader = fragS.read()

        return self.renderEngine.context.program(vertex_shader = vertexShader, fragment_shader = fragmentShader)

    def render(self):
        self.update()
        self.vertexArray.render()

    def destroy(self):
        self.vertexBufferObj.destroy()
        #self.shaderProgram.release()
        self.vertexArray.release()