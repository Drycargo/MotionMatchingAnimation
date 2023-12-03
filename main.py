import numpy as np

from models.BvhModel import BvhAnimation
from viewer.SimpleViewer import SimpleViewer
from viewer.openGLViewer.Light import Light
from viewer.openGLViewer.OpenGlEngine import OpenGlEngine
from viewer.openGLViewer.GeometryModel import GeometryModel
from viewer.openGLViewer.modelTypes.RotateModel import RotateModel
import glm
import moderngl as mgl
import pygame as pg

def startSimpleViewer():
    anim = BvhAnimation(filePath="animations/sprint1_subject2.bvh", useRad=False)
    #anim = BvhAnimation(filePath="animations/09_01.bvh", useRad=False)
    simpleViewer = SimpleViewer()
    simpleViewer.loadAnimation(anim)
    simpleViewer.startAnimation()

def startOpenGlViewer():
    openGlViewer = OpenGlEngine()
    # openGlViewer.addModel([(-0.5, -0.5, 0), (0.5, -0.5, 0), (0, 0.5, 0)], [(0, 1, 2)])
    sampleLight = Light(pos=glm.vec3(0, 0, 1), color=glm.vec3(1, 1, 1))
    openGlViewer.addLight(sampleLight)
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

    model = RotateModel(
        openGlViewer,
        dataIndPairs=[
            (verticeUv, triangleIndiceUv),
            (verticeNormal, triangleIndiceNormal),
            (verticePos, triangleIndicePos)],
        axis=glm.sphericalRand(1.0),
        rotationSpeed=0.02)
    model.addTexture("\\textures\\img_1.png")
    openGlViewer.addModel(model)
    openGlViewer.run()

if __name__ == "__main__":
    print("main starts.")
    #startSimpleViewer()
    startOpenGlViewer()

    print("main done.")