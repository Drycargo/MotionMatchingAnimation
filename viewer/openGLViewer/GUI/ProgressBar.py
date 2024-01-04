import pygame as pg
from utils.MouseState import MouseState
from viewer.openGLViewer.GUI.BaseGui import BaseGui


class ProgressBar(BaseGui):
    def __init__(self, renderEngine, size, topLeftPos):
        shader = renderEngine.meshManager.vertArrayManager.shaderPrograms.getShaderProgram("progressBar", "default2D")
        self.initializeGeoData(renderEngine, shader, size, topLeftPos)

    def update(self, mouseState: MouseState, inside: bool):
        self.shader['inGeneration'] = False
        animDB = self.renderEngine.animDatabase

        if inside and mouseState.leftDown:
            newProgress = \
                (pg.mouse.get_pos()[0] - self.boundaries['left']) / (self.boundaries['right']- self.boundaries['left'])
            newFrame = int(animDB.frameCount * newProgress)
            animDB.currentFrame = newFrame
            animDB.updateAnimation(newFrame)
            self.shader['progress'] = newProgress
        else:
            self.shader['progress'] = animDB.currentFrame / animDB.frameCount
