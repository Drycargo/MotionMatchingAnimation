from viewer.openGLViewer.GeometryModel import GeometryModel
from viewer.openGLViewer.modelTypes.UnlitModel import UnlitModel, ReferenceGridModel


class Scene:
    def __init__(self, renderEngine):
        self.renderEngine = renderEngine
        self.objects = set()
        self.refPlane = ReferenceGridModel(
            renderEngine=renderEngine,
            vertexArrayName="RefPlane",
            initScale=(1250,1,1250)
        )

        # Add Reference Plane
        self.addObject(self.refPlane)

    def addObject(self, model: GeometryModel):
        self.objects.add(model)

    def render(self):
        for obj in self.objects:
            obj.render()

    def clear(self):
        self.objects = set()
        self.addObject(self.refPlane)