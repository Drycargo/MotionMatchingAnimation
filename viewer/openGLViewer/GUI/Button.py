from utils.MouseState import MouseState
from viewer.openGLViewer.GUI.BaseGui import BaseGui

class Button(BaseGui):
    def __init__(self, renderEngine, size, topLeftPos, shader, texture, actionListener = None):
        super().__init__(renderEngine, size, topLeftPos, shader, texture)
        self.onClick = actionListener
        self.pressed = False

    def update(self, mouseState: MouseState, inside: bool):
        if inside:
            if mouseState.leftDown:
                self.shader['hover'] = False
                self.shader['clicked'] = True
                if not self.pressed:
                    if self.onClick:
                        self.onClick()
                    self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                self.shader['hover'] = True
                self.shader['clicked'] = False
        else:
            if self.pressed:
                self.pressed = False
            self.shader['hover'] = False
            self.shader['clicked'] = False

class PlayPauseButton(Button):
    def __init__(self, renderEngine, size, topLeftPos):
        meshManager = renderEngine.meshManager
        shader = meshManager.vertArrayManager.shaderPrograms.getShaderProgram("playPauseButton", "default2D")
        playTexStruct = meshManager.textureManager.getTextureAndId("play_icon.png")
        pauseTex, pauseTexId = meshManager.textureManager.getTextureAndId("pause_icon.png")
        super().__init__(renderEngine, size, topLeftPos, shader, playTexStruct, lambda: renderEngine.pauseOrPlay())
        self.shader['u_texture_1'] = pauseTexId
        pauseTex.use(pauseTexId)

    def update(self, mouseState: MouseState, inside: bool):
        super(PlayPauseButton, self).update(mouseState, inside)
        self.shader['paused'] = self.renderEngine.paused
