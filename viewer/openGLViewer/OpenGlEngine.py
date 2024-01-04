import glm
import pygame as pg
import moderngl as mgl

from models.BvhModel import BvhAnimation
from utils.MouseState import MouseState
from viewer.openGLViewer.Camera import Camera
from viewer.openGLViewer.GUI.BaseGui import BaseGui
from viewer.openGLViewer.GUI.Button import Button, PlayPauseButton
from viewer.openGLViewer.GUI.ProgressBar import ProgressBar
from viewer.openGLViewer.GeometryModel import GeometryModel
from viewer.openGLViewer.Scene import Scene
from viewer.openGLViewer.Mesh import MeshManager
from tkinter import filedialog
import tkinter as tk

class OpenGlEngine:
    def __init__(self, dim = (720, 540), backgroundColor = (0.4, 0.4, 0.4, 1.0), fps = 60, animDatabase = None):
        self.WINDOW_DIM = dim
        self.BG_COLOR = backgroundColor
        self.mouseState = MouseState()

        pg.init()
        self.setupGlAttributes()
        self.window = pg.display.set_mode(size = self.WINDOW_DIM, flags = pg.OPENGL | pg.DOUBLEBUF)

        self.context = mgl.create_context()
        self.context.enable(flags= mgl.DEPTH_TEST|mgl.CULL_FACE|mgl.ONE_MINUS_SRC_ALPHA)

        self.clock = pg.time.Clock()
        self.time = 0
        self.objects = set()
        self.lights = set()

        self.camera = Camera(self, pos=glm.vec3(500, 500, 500), far=1500, yaw = -135, pitch = -45)
        self.meshManager = MeshManager(self)
        self.scene = Scene(self)

        self.paused = False

        if animDatabase:
            self.setAnimDataBase(animDatabase)
        else:
            self.animDatabase = None
            self.FPS = fps

        self.initializeUIs()

    def setAnimDataBase(self, animDatabase):
        self.animDatabase = animDatabase
        self.scene.clear()
        animDatabase.createModels(self)
        self.FPS = 1.0 / animDatabase.frameDuration

    def initializeUIs(self):
        self.uis = []
        textureManager = self.meshManager.textureManager

        # Play/ Pause Button
        playPauseButton = PlayPauseButton(self, (32, 32), (20, 20))
        self.uis.append(playPauseButton)

        # Import Button
        importTexStruct = textureManager.getTextureAndId("import_icon.png")
        buttonShader = self.meshManager.vertArrayManager.shaderPrograms.getShaderProgram("button", "default2D")
        importButton = Button(self, (32, 32), (60, 20), buttonShader, importTexStruct, self.loadNewAnim)
        self.uis.append(importButton)

        # Progress Bar
        progressBarLen = 300
        progressBar = ProgressBar(self, (progressBarLen, 15), \
                                  ((self.WINDOW_DIM[0] - progressBarLen)/2, self.WINDOW_DIM[1] - 30))
        self.uis.append(progressBar)

    def loadNewAnim(self):
        root = tk.Tk()
        filename = filedialog.askopenfilename(filetypes = [("BVH Animation", ".bvh")])

        if filename:
            self.setAnimDataBase(BvhAnimation(filePath=filename, useRad=False))
        root.destroy()

    def renderUi(self):
        for ui in self.uis:
            ui.renderUi()

    def pauseOrPlay(self):
        self.paused = (not self.paused)

    def addLight(self, newLight):
        self.lights.add(newLight)

    def setupGlAttributes(self):
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

    def destroy(self):
        self.meshManager.destroy()
        for ui in self.uis:
            ui.destroy()

    def checkEvents(self):
        scrolled = False
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                self.destroy()
                return False

            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.pauseOrPlay()

            if event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
                buttonState = (event.type == pg.MOUSEBUTTONDOWN)
                if event.button == pg.BUTTON_LEFT:
                    self.mouseState.leftDown = buttonState
                elif event.button == pg.BUTTON_MIDDLE:
                    self.mouseState.midDown = buttonState
                elif event.button == pg.BUTTON_RIGHT:
                    self.mouseState.rightDown = buttonState

            if event.type == pg.MOUSEWHEEL:
                scrolled = True
                self.mouseState.relScroll = event.y

        if not scrolled:
            self.mouseState.relScroll = 0

        return True

    def render(self):
        # Clear with color
        self.context.clear(color = self.BG_COLOR)
        self.scene.render()
        self.renderUi()
        # Swap buffer
        pg.display.flip()

    def checkUis(self):
        self.mouseState.operatingUi = False
        for ui in self.uis:
            mouseInside = ui.mouseInside()
            if mouseInside:
                if not self.mouseState.operatingUi:
                    self.mouseState.operatingUi = True
            ui.update(self.mouseState, mouseInside)

    def run(self):
        while self.checkEvents():
            self.camera.update()
            self.checkUis()
            if (not self.paused) and self.animDatabase:
                self.time = pg.time.get_ticks() * 0.001
                self.animDatabase.update()
                self.clock.tick(self.FPS)
            self.render()

    def addModel(self, geoModel: GeometryModel):
        self.scene.addObject(geoModel)
