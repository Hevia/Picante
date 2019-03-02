import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import math

style.use('fivethirtyeight')


class Sensor:
    # Get figure objects from sensor to the

    # Store information
    def __init__(self):
        self.values = list() # Voltage values on the y-axis
        self.mapped_data = list() # The mapped values from the delta voltage values
        self.time = list()  # Time values on the x-axis
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)

    def mapData(self, data):
        delta_y = data - self.values[len(self.values) - 1]
        x = 0
        scaling = 2

        if delta_y > 0:
            x = math.floor(math.log(delta_y/scaling, 2))
        elif delta_y < 0:
            x = math.ceil(math.log(delta_y/scaling, 2))

        if x > 4:
            x = 4
        elif x < -4:
            x = -4
        return x

    def addData(self, time_stamp, data):

        # Initial instance of the list
        if len(self.values) == 0:
            self.values.append(data)
            self.time.append(time_stamp)
        else:
            self.values.append(data)
            self.time.append(time_stamp)
            self.mapped_data.append(self.mapData(data))



    def animate(self,i):
        xs = self.time
        ys = self.values
        self.ax1.clear()
        self.ax1.plot(xs, ys)

    def makeFigure(self):
        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)
        plt.show()


# Test Code
# s = Sensor()
# s.addData(3295, 512)
# s.addData(3347, 511)
# s.addData(3553, 512)
# s.makeFigure();