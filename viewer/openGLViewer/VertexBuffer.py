import numpy as np

class VertexBufferManager:
    def __init__(self, context):
        self.context = context
        self.vertexBuffers = {}

        # Add Cube
        self.addVertexBuffer(
            'Cube',
            dataIndPairs = VertexBufferManager.getCubeIndPairs(),
            config = {'format': '2f 3f 3f', 'attr': ['in_texcoord_0', 'in_normal', 'in_position']}
        )

        # Add Plane
        self.addVertexBuffer(
            'Plane',
            dataIndPairs= VertexBufferManager.getPlaneIndPairs(),
            config={'format': '3f', 'attr': ['in_position']}
        )

    def addVertexBuffer(self, name, dataIndPairs, config):
        newBufferObj = VertexBufferObj(self.context, rawData = dataIndPairs, config = config)
        self.vertexBuffers[name] = newBufferObj
        return newBufferObj

    def getVertexBufferTuple(self, name):
        vertBufferObj = self.vertexBuffers[name]
        return (vertBufferObj.bufferObject, vertBufferObj.vertDataFormat, vertBufferObj.vertDataAttr)

    def destroy(self):
        for buffer in self.vertexBuffers.values():
            buffer.destroy()

    @staticmethod
    def getPlaneIndPairs():
        verticePos = [
            (-0.5, 0, -0.5), (0.5, 0, -0.5),
            (-0.5, 0, 0.5), (0.5, 0, 0.5)
        ]
        triangleIndicePos = [
            (0, 2, 1), (1, 2, 3)
        ]

        return [
            (verticePos, triangleIndicePos)]

    @staticmethod
    def getRectPairs(sizeNorm, topLeftPosNorm):
        verticePos = [
            topLeftPosNorm,
            (topLeftPosNorm[0] + sizeNorm[0], topLeftPosNorm[1]),
            (topLeftPosNorm[0], topLeftPosNorm[1] - sizeNorm[1]),
            (topLeftPosNorm[0] + sizeNorm[0], topLeftPosNorm[1] - sizeNorm[1])
        ]

        verticeUv = [(0, 0), (1, 0), (0, 1), (1, 1)]

        triangleIndicePos = [
            (0, 2, 1), (1, 2, 3)
        ]

        return [
            (verticeUv, triangleIndicePos),
            (verticePos, triangleIndicePos)]

    @staticmethod
    def getCubeIndPairs():
        verticePos = [
            (-0.5, 0.5, 0.5), (0.5, 0.5, -0.5),  # 0 1
            (-0.5, -0.5, 0.5), (0.5, -0.5, -0.5),  # 2 3
            (0.5, 0.5, 0.5), (-0.5, 0.5, -0.5),  # 4 5
            (0.5, -0.5, 0.5), (-0.5, -0.5, -0.5),  # 6 7
        ]
        triangleIndicePos = [
            (0, 4, 5), (4, 1, 5),
            (2, 6, 0), (6, 4, 0),
            (6, 3, 4), (3, 1, 4),
            (2, 7, 6), (6, 7, 3),
            (2, 0, 7), (7, 0, 5),
            (1, 3, 7), (7, 5, 1)
        ]

        verticeUv = [(0, 0), (1, 0), (0, 1), (1, 1)]
        triangleIndiceUv = [
            (0, 2, 1), (2, 3, 1),
            (2, 3, 0), (3, 1, 0),
            (2, 3, 0), (3, 1, 0),
            (0, 2, 1), (1, 2, 3),
            (3, 1, 2), (2, 1, 0),
            (0, 2, 3), (3, 1, 0)
        ]

        verticeNormal = [(0, 0, 1), (0, 0, -1), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
        triangleIndiceNormal = [
            (4, 4, 4), (4, 4, 4),
            (0, 0, 0), (0, 0, 0),
            (2, 2, 2), (2, 2, 2),
            (5, 5, 5), (5, 5, 5),
            (3, 3, 3), (3, 3, 3),
            (1, 1, 1), (1, 1, 1)
        ]

        return [
            (verticeUv, triangleIndiceUv),
            (verticeNormal, triangleIndiceNormal),
            (verticePos, triangleIndicePos)]

class VertexBufferObj:
    def __init__(self, context, rawData, config):
        self.context = context
        self.bufferObject = self.createBufferObject(rawData)
        self.vertDataFormat: str = config['format']
        self.vertDataAttr: list = config['attr']

    @staticmethod
    def createVertStructArray(dataIndexPairs):
        rawVertexData = []

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
                rawVertexData.append(resultProperties)
        return np.array(rawVertexData, dtype='f4')

    def createBufferObject(self, dataIndexPairs):
        return self.context.buffer(VertexBufferObj.createVertStructArray(dataIndexPairs))

    def destroy(self):
        self.bufferObject.release()