import pygame as pg

from utils.MouseState import MouseState
from viewer.openGLViewer.VertexBuffer import VertexBufferManager, VertexBufferObj


class BaseGui:
    def __init__(self, renderEngine, size, topLeftPos, shader, texture):
        self.texture, texId = texture
        self.renderEngine = renderEngine
        self.boundaries = {
            'left': topLeftPos[0],
            'right': topLeftPos[0] + size[0],
            'top': topLeftPos[1],
            'bottom': topLeftPos[1] + size[1],
        }

        config2D = {'format': '2f 2f', 'attr': ['in_texcoord_0', 'in_position']}

        dimRatios = (renderEngine.WINDOW_DIM[0] / 2.0, renderEngine.WINDOW_DIM[1] / 2.0)
        indexPairs = VertexBufferManager.getRectPairs( \
            (size[0] / dimRatios[0], size[1] / dimRatios[1]), \
            (topLeftPos[0] / dimRatios[0] - 1.0, -(topLeftPos[1] / dimRatios[1] - 1.0)))
        self.shader = shader
        self.bufferObj = VertexBufferObj(renderEngine.context, indexPairs, config2D)
        self.vertArray = renderEngine.context.vertex_array(
            shader,
            [(self.bufferObj.bufferObject, self.bufferObj.vertDataFormat, *self.bufferObj.vertDataAttr)])

        shader['u_texture_0'] = texId
        self.texture.use(texId)

    def mouseInside(self):
        mouseX, mouseY = pg.mouse.get_pos()
        return self.boundaries['left'] <= mouseX <= self.boundaries['right']\
            and self.boundaries['top'] <= mouseY <= self.boundaries['bottom']

    def renderUi(self):
        self.vertArray.render()

    def destroy(self):
        self.vertArray.release()
        self.bufferObj.destroy()

    def update(self, mouseState: MouseState, inside: bool):
        pass