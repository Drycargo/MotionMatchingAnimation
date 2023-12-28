import re
import pygame as pg
import moderngl as mgl

class TextureManager:
    def __init__(self, context):
        self.context = context
        self.textures = {}
        self.textureCount = 0

    def getTextureAndId(self, textureName, flip = False):
        if textureName in self.textures:
            return self.textures[textureName]['texture'], self.textures[textureName]['Id']

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

        self.textures[textureName] = {'texture': newTexture, 'Id': self.textureCount}
        self.textureCount += 1
        return self.textures[textureName]['texture'], self.textures[textureName]['Id']

    def destroy(self):
        for textureStruct in self.textures.values():
            textureStruct['texture'].release()