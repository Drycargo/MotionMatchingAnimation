import glm

from viewer.openGLViewer.VertexBuffer import VertexBufferManager, VertexBufferObj


class BaseGui:
    def __init__(self, renderEngine, size, topLeftPos, shader, texture):
        self.texture = texture
        self.renderEngine = renderEngine

        config2D = {'format': '2f 2f', 'attr': ['in_texcoord_0', 'in_position']}

        dimRatios = (renderEngine.WINDOW_DIM[0] /2.0, renderEngine.WINDOW_DIM[1] /2.0)
        indexPairs = VertexBufferManager.getRectPairs(\
            (size[0]/renderEngine.WINDOW_DIM[0], size[1]/renderEngine.WINDOW_DIM[1]), \
            (topLeftPos[0]/dimRatios[0] - 1.0, -(topLeftPos[1]/dimRatios[1] - 1.0)))
        self.shader = shader
        self.bufferObj = VertexBufferObj(renderEngine.context, indexPairs, config2D)
        self.vertArray = renderEngine.context.vertex_array(
            shader,
            [(self.bufferObj.bufferObject, self.bufferObj.vertDataFormat, *self.bufferObj.vertDataAttr)])

        shader['u_texture_0'] = 1
        self.texture.use(1)

    def renderUi(self):
        self.vertArray.render()

    def destroy(self):
        self.vertArray.release()
        self.bufferObj.destroy()