import re
import pygame as pg
import moderngl as mgl

class TextureManager:
    def __init__(self, context):
        self.context = context
        self.textures = {}

    def getTexture(self, textureName, flip = False):
        if textureName in self.textures:
            return self.textures[textureName]

        parentDir = '\\'.join(re.split('\\\\|/', __file__)[:-1])
        rawTexture = pg.image.load("{}\\textures\\{}".format(parentDir, textureName)).convert()

        if flip:
            rawTexture = pg.transform.flip(rawTexture, flip_x = False, flip_y= True)

        newTexture = self.context.texture(
            size = rawTexture.get_size(),
            components = 3,
            data = pg.image.tostring(rawTexture, 'RGB'))

        # Enable Mipmap
        newTexture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        newTexture.build_mipmaps()

        newTexture.anisotropy = 32.0

        self.textures[textureName] = newTexture
        return newTexture

    def destroy(self):
        for texture in self.textures.values():
            texture.release()