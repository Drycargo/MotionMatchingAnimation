import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

DIMENSION = 200.0

class SimpleViewer:
    def __init__(self):
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111, projection="3d")
        self.animationDatabase = None
        self.animation = None

    def loadAnimation(self, animationDatabase):
        self.animationDatabase = animationDatabase

    def startAnimation(self):
        self.animation = FuncAnimation(fig = self.fig, func = self.update, \
                                       frames = self.animationDatabase.frameCount, \
                                       interval = 1000 * self.animationDatabase.frameDuration)
        plt.show()

    def update(self, frame):
        self.axes.clear()
        plt.title("Simple Viewer")
        self.axes.set_xlim(-DIMENSION,DIMENSION)
        self.axes.set_ylim(-DIMENSION,DIMENSION)
        self.axes.set_zlim(-DIMENSION,DIMENSION)

        self.animationDatabase.updateAnimation(frame)
        self.draw(self.animationDatabase.getRenderData())

    def draw(self, data):
        for pointPair in data:
            self.axes.plot(xs=[pointPair[0][0], pointPair[1][0]],
                     zs=[pointPair[0][1], pointPair[1][1]],
                     ys=[pointPair[0][2], pointPair[1][2]], c='blue', lw=1.5)
