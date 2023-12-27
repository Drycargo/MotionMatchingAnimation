import sys

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
import imgui

def startSimpleViewer():
    anim = BvhAnimation(filePath="animations/sprint1_subject2.bvh", useRad=False)
    #anim = BvhAnimation(filePath="animations/09_01.bvh", useRad=False)
    simpleViewer = SimpleViewer()
    simpleViewer.loadAnimation(anim)
    simpleViewer.startAnimation()

def startOpenGlViewer():

    anim = BvhAnimation(filePath="animations/sprint1_subject4.bvh", useRad=False)
    openGlViewer = OpenGlEngine(animDatabase=anim)
    sampleLight = Light(pos=glm.vec3(0, 0, 200), color=glm.vec3(1, 1, 1))
    openGlViewer.addLight(sampleLight)
    anim.createModels(openGlViewer)
    openGlViewer.run()
    '''
    openGlViewer = OpenGlEngine()
    sampleLight = Light(pos=glm.vec3(0, 0, 1), color=glm.vec3(1, 1, 1))
    openGlViewer.addLight(sampleLight)
    model = GeometryModel(
        openGlViewer,
        vertexArrayName= 'Cube',
        textureName = "img_1.png",
        initRot=(0,0,45),
        initScale=(2,1,1)
    )
    openGlViewer.addModel(model)
    openGlViewer.run()
    '''

if __name__ == "__main__":
    print("main starts.")
    #startSimpleViewer()
    startOpenGlViewer()

    print("main done.")
