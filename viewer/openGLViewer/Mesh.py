from viewer.openGLViewer.VertexArray import VertexArrayManager
from viewer.openGLViewer.Texture import TextureManager

class MeshManager:
    def __init__(self, renderEngine):
        self.renderEngine = renderEngine
        self.vertArrayManager = VertexArrayManager(self.renderEngine.context)
        self.textureManager = TextureManager(self.renderEngine.context)

    def destroy(self):
        self.vertArrayManager.destroy()
        self.textureManager.destroy()