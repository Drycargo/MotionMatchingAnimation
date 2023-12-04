import glm
import pygame as pg
import moderngl as mgl
from utils.MouseState import MouseState
from viewer.openGLViewer.Camera import Camera
from viewer.openGLViewer.Scene import Scene
from viewer.openGLViewer.ShaderPrograms import ShaderPrograms
from viewer.openGLViewer.Mesh import MeshManager

class OpenGlEngine:
    def __init__(self, dim = (720, 540), backgroundColor = (0.8, 0.8, 0.8, 1.0), fps = 60, animDatabase = None):
        self.WINDOW_DIM = dim
        self.BG_COLOR = backgroundColor
        self.mouseState = MouseState()

        pg.init()
        self.setupGlAttributes()
        pg.display.set_mode(size = self.WINDOW_DIM, flags = pg.OPENGL | pg.DOUBLEBUF)

        self.context = mgl.create_context()
        self.context.enable(flags= mgl.DEPTH_TEST|mgl.CULL_FACE)

        self.clock = pg.time.Clock()
        self.time = 0
        self.objects = set()
        self.lights = set()

        self.camera = Camera(self, pos=glm.vec3(500, 500, 500), far=1500, yaw = -135, pitch = -45)
        self.meshManager = MeshManager(self)
        self.scene = Scene(self)
        self.animDatabase = animDatabase

        if self.animDatabase:
            self.FPS = 1.0/self.animDatabase.frameDuration
        else:
            self.FPS = fps

    def addLight(self, newLight):
        self.lights.add(newLight)

    def setupGlAttributes(self):
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

    def destroy(self):
        self.meshManager.destroy()

    def checkEvents(self):
        scrolled = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                self.destroy()
                return False

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
        # Swap buffer
        pg.display.flip()

    def run(self):
        while self.checkEvents():
            self.time = pg.time.get_ticks() * 0.001
            self.camera.update()
            if self.animDatabase:
                self.animDatabase.update()
            self.render()
            self.clock.tick(self.FPS)

    def addModel(self, geoModel):
        self.scene.addObject(geoModel)
