from viewer.openGLViewer.GeometryModel import GeometryModel
from viewer.openGLViewer.modelTypes.UnlitModel import UnlitModel, ReferenceGridModel


class Scene:
    def __init__(self, renderEngine):
        self.renderEngine = renderEngine
        self.objects = set()

        # Add Reference Plane
        self.addObject(ReferenceGridModel(
            renderEngine=renderEngine,
            vertexArrayName="RefPlane",
            initScale=(1250,1,1250)
        ))

    def addObject(self, model: GeometryModel):
        self.objects.add(model)

    def render(self):
        for obj in self.objects:
            obj.render()