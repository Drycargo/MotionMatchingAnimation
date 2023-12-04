class Light:
    def __init__(self, pos, color):
        self.position = pos
        self.ambientI = 0.3 * color
        self.diffuseI = 0.8 * color
        self.specularI = 1 * color