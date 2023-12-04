from viewer.openGLViewer.GeometryModel import GeometryModel


class UnlitModel(GeometryModel):
    def update(self):
        self.updateMatrices()
        self.setMatrices()

class ReferenceGridModel(UnlitModel):
    def initialize(self):
        super(ReferenceGridModel, self).initialize()

        self.shaderProgram['gridWidth'] = 75.0
        self.shaderProgram['lineWidth'] = 0.85
        self.shaderProgram['axisAmp'] = 3.0
