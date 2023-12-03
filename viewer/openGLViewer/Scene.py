class Scene:
    def __init__(self, renderEngine):
        self.renderEngine = renderEngine
        self.objects = set()

    def addObject(self, model):
        self.objects.add(model)

    def render(self):
        for obj in self.objects:
            obj.render()