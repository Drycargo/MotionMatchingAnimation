#from models.BvhModel import BvhAnimation, BvhNode
import numpy as np

from viewer.openGLViewer.GeometryModel import GeometryModel
from utils.MatrixUtils import Dir, getRotMat
import glm
import math

RIG_WIDTH = 0.1
END_SITE_PREFIX = "End Site: "

class RigModel(GeometryModel):
    def __init__(self, renderEngine, vertexArrayName, animDatabase, nodeName: str, textureName=None):
        self.isEndSite = nodeName.startswith(END_SITE_PREFIX)

        if self.isEndSite:
            nodeName = nodeName[len(END_SITE_PREFIX):]
        self.nodeName = nodeName
        self.animDatabase = animDatabase
        node = animDatabase.getNode(nodeName)

        #print(node)

        rigOffset = node.endsiteOffset if self.isEndSite else node.offsetValues
        rigLength = glm.length(rigOffset)
        rotZ = math.asin(rigOffset[1] / rigLength)
        rotY = -math.atan2(rigOffset[2], rigOffset[0])

        self.initialRotationMat = getRotMat(rotY, Dir.Y, True) @ getRotMat(rotZ, Dir.Z, True)

        super(RigModel, self).__init__(renderEngine, vertexArrayName, textureName = textureName, \
                                       initScale = (rigLength, RIG_WIDTH * rigLength, RIG_WIDTH * rigLength))

    def getModelMat(self):
        # Init
        modelMatrix = glm.mat4()

        (centralPos, rotationMat) = self.animDatabase.getNodeTransformTuple(self.nodeName, self.isEndSite)

        # Translation
        modelMatrix = glm.translate(modelMatrix, centralPos)

        # Rotation
        modelMatrix = modelMatrix @ glm.mat4(rotationMat @ self.initialRotationMat)

        # Scale
        modelMatrix = self.scaleMatrix(modelMatrix)
        return modelMatrix