import glm
import numpy as np

from utils.MatrixUtils import Dir, getRotMat
from viewer.openGLViewer.OpenGlEngine import OpenGlEngine
from viewer.openGLViewer.modelTypes.RigModel import RigModel, END_SITE_PREFIX

ROOT_STR = "root"
JOINT_STR = "joint"
END_SITE_STR = "end site"
OFFSET_STR = "offset"
CHANNELS_STR = "channels"
FRAME_COUNT_STR = "frames:"
FRAME_TIME_STR = "frame time:"

CHANNEL_ROTATION_STR = "rotation"
CHANNEL_POSITION_STR = "position"

class BvhNode:
    def __init__(self, name, parent = None):
        self.name = name
        self.parent = parent

        self.offsetValues = None
        self.channelNames = None
        self.channelOffset = None
        self.endsiteOffset = None

        self.currentRotMat = None
        self.currentWorldPos = None

    def __str__(self):
        return "{}: PARENT:{}; OFFSET: {}; CHANNELS: {} -> {}; endsite: {}; currentRot: {}".format(\
            self.name, self.parent, ','.join([str(val) for val in self.offsetValues]), \
            ','.join(self.channelNames), str(self.channelOffset), \
            ','.join([str(val) for val in self.endsiteOffset]) if self.endsiteOffset else "None", \
            str(self.currentRotMat))

class BvhAnimation:
    def __init__(self, filePath, useRad = True):
        self.bvhNodes = {}
        self.traverseOrder = []
        self.rootNames = []
        self.frames = []
        self.frameDuration = 0.04167 # 24fps
        self.frameCount = 0
        self.currentFrame = 0
        self.useRad = useRad
        with open(filePath) as bvhContent:
            self.parseFile(bvhContent)

    def getNode(self, nodeName):
        return self.bvhNodes[nodeName]

    def update(self):
        self.updateAnimation(self.currentFrame)
        self.currentFrame +=1
        if self.currentFrame > self.frameCount:
            self.currentFrame = 0

    def updateAnimation(self, frameNumber):
        if frameNumber < 0 or frameNumber >= len(self.frames):
            # frame out of range
            return

        # First Round: get local position
        for nodeName in self.traverseOrder:
            currNode = self.bvhNodes[nodeName]

            posOffset = currNode.offsetValues

            #parentRotMat = self.bvhNodes[currNode.parent].currentRotMat if currNode.parent else np.eye(3)
            currNode.currentRotMat = self.bvhNodes[currNode.parent].currentRotMat if currNode.parent else glm.mat3()

            for i in range(0, len(currNode.channelNames)):
                channelName = currNode.channelNames[i]
                channelVal = self.frames[frameNumber][currNode.channelOffset + i]

                # Get channel axis
                axis = channelName[0].lower()
                if axis == 'x':
                    axis = Dir.X
                elif axis == 'y':
                    axis = Dir.Y
                else:
                    axis = Dir.Z

                channelType = channelName[1:].lower()
                if channelType == CHANNEL_ROTATION_STR:
                    currNode.currentRotMat = currNode.currentRotMat @ getRotMat(channelVal, axis, useRad= self.useRad)
                elif channelType == CHANNEL_POSITION_STR:
                    # Root obj
                    posOffset[axis.value] = channelVal

            if currNode.parent:
                # not root
                currNode.currentWorldPos = self.bvhNodes[currNode.parent].currentWorldPos \
                                           + self.bvhNodes[currNode.parent].currentRotMat @ posOffset
            else:
                # root
                currNode.currentWorldPos = posOffset

    def getNodeTransformTuple(self, nodeName, isEnsite = False):
        # Fetch central position and rotation (based on parent node) matrix
        centralPos = None
        rotationMat = None
        if isEnsite:
            currNode: BvhNode = self.bvhNodes[nodeName]
            centralPos = currNode.currentWorldPos + 0.5 * currNode.currentRotMat @ currNode.endsiteOffset
            rotationMat = currNode.currentRotMat
        else:
            currNode: BvhNode = self.bvhNodes[nodeName]
            parentNode: BvhNode = self.bvhNodes[currNode.parent]
            centralPos = (currNode.currentWorldPos + parentNode.currentWorldPos) / 2
            rotationMat = parentNode.currentRotMat

        return (centralPos, rotationMat)

    def getSimpleRenderData(self):
        result = []

        for nodeName in self.traverseOrder:
            currNode = self.bvhNodes[nodeName]
            if not currNode.parent:
                continue

            parentNode = self.bvhNodes[currNode.parent]
            result.append((parentNode.currentWorldPos, currNode.currentWorldPos))

            if currNode.endsiteOffset:
                result.append((currNode.currentWorldPos, currNode.currentWorldPos + currNode.currentRotMat @ currNode.endsiteOffset))

        return result

    def createModels(self, renderEngine: OpenGlEngine):
        for node in self.bvhNodes.values():
            if node.name in self.rootNames:
                continue
            newRigModel = RigModel(
                renderEngine = renderEngine,
                vertexArrayName = 'Cube',
                animDatabase = self,
                nodeName= node.name,
                textureName='red pixel.png'
            )
            renderEngine.addModel(newRigModel)

            if node.endsiteOffset and glm.length(node.endsiteOffset) > 0:
                endsiteModel = RigModel(
                    renderEngine = renderEngine,
                    vertexArrayName = 'Cube',
                    animDatabase = self,
                    nodeName= "{}{}".format(END_SITE_PREFIX, node.name),
                    textureName='white pixel.png'
                )
                renderEngine.addModel(endsiteModel)

    def parseFile(self, bvhContent):
        self.readingHierarchy = True
        currChannelOffset = 0
        nodeStack = [None]

        currentNodeName = None
        handlingEndSite = False

        for rawLine in bvhContent.readlines():
            rawLine = rawLine.strip()
            line = rawLine.lower()

            # Read Hierarchy/ Animation Frames
            if line.startswith("hierarchy"):
                self.readingHierarchy = True
                continue
            elif line.startswith("motion"):
                self.readingHierarchy = False
                continue
            
            if self.readingHierarchy:
                # Initialize Hierarchy
                if line.startswith(ROOT_STR) or line.startswith(JOINT_STR):
                    # Create Nodes
                    currentNodeName = rawLine.split()[-1]
                    self.bvhNodes[currentNodeName] = BvhNode(currentNodeName, nodeStack[-1])
                    self.traverseOrder.append(currentNodeName)
                    nodeStack.append(currentNodeName)

                    if line.startswith(ROOT_STR):
                        # Root node
                        self.rootNames.append(currentNodeName)
                        self.offsetValues = [0, 0, 0]
                elif line.startswith(END_SITE_STR):
                    handlingEndSite = True
                elif line.startswith(OFFSET_STR):
                    # Update Node offset
                    # OFFSET 0.0 0.0 0.0
                    offsetVal = [float(val) for val in line.split()[1:]]
                    if handlingEndSite:
                        self.bvhNodes[nodeStack[-1]].endsiteOffset = offsetVal
                    else:
                        self.bvhNodes[currentNodeName].offsetValues = offsetVal
                elif line.startswith(CHANNELS_STR):
                    # Update Channel
                    # CHANNELS 3 xr yr zr
                    channelLineFields = line.split()
                    self.bvhNodes[currentNodeName].channelNames = channelLineFields[2:]
                    self.bvhNodes[currentNodeName].channelOffset = currChannelOffset
                    currChannelOffset += int(channelLineFields[1])
                elif line.startswith("}"):
                    if handlingEndSite:
                        handlingEndSite = False
                    else:
                        nodeStack.pop()
            else:
                # Read Animation
                if line.startswith(FRAME_COUNT_STR):
                    self.frameCount = int(line.split()[-1])
                elif line.startswith(FRAME_TIME_STR):
                    self.frameDuration = float(line.split()[-1])
                else:
                    self.frames.append([float(val) for val in line.split()])
    