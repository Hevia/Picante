import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

class Sensor:
    # Get figure objects from sensor to the

    # Store information
    def __init__(self):
        self.values = list()
        self.time = list()
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)

    def addData(self, time_stamp, data):
        self.values.append(data)
        self.time.append(time_stamp)

    def animate(self,i):
        xs = self.time
        ys = self.values
        self.ax1.clear()
        self.ax1.plot(xs, ys)

    def makeFigure(self):
        animation.FuncAnimation(self.fig, self.animate, interval=1000)
        plt.show()


# Test Implementation
# s = Sensor()
# s.addData(1, 0)
# s.addData(2, 2)
# s.addData(3, 3)
# s.makeFigure();


# Test case, make sensorData