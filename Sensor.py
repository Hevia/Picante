import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import math
import csv

style.use('fivethirtyeight')


class Sensor:
    # Get figure objects from sensor to the

    # Store information
    def __init__(self, n_sec=0.25, scaling=0.09):
        self.n_sec = n_sec
        self.interval = 0.0
        self.scaling = scaling
        self.values = list() # Voltage values on the y-axis
        self.mapped_data = list() # The mapped values from the delta voltage values
        self.mapped_time = list() # The ms values converted to seconds
        self.time = list()  # Time values on the x-axis
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)

    def mapData(self):
        slope = 0
        mapped_val = 0
        loop_interval = self.calc_interval() 
        loop_interval = math.ceil(loop_interval)
        loop_interval = int(loop_interval)

        for i in range(0, len(self.values)-1, loop_interval):
            if i >= len(self.values) or i+loop_interval >= len(self.values):
                break
            else:
                slope = (self.values[i+loop_interval] - self.values[i]) / loop_interval
                slope /= self.scaling

                if slope < 0:
                    slope = math.floor(slope)
                elif slope > 0:
                    slope = math.ceil(slope)

                if slope > 4:
                    slope = 4
                elif slope < -4:
                    slope = -4
                self.mapped_data.append(int(slope))
       

    # This calculates the total length of the recording
    def mapTime(self):
        return self.time[len(self.time)-1] / 1000

    def calc_interval(self):
        print(self.n_sec)
        print((len(self.values)/self.mapTime()))
        self.interval = self.n_sec * (len(self.values)/self.mapTime())
        return self.interval

    def addData(self, time_stamp, data):
        self.values.append(data)
        self.time.append(time_stamp)

        # We won't calculate data until we hit certain intervals of the list
        # if len(self.values) <= self.interval:
        #     self.values.append(data)
        #     self.time.append(time_stamp)
        # else:
        #     self.values.append(data)
        #     self.time.append(time_stamp)
        #     self.mapped_data.append(self.mapData(data))
        #     self.mapped_time.append(self.mapTime(time_stamp))


    def readData(self, file_name):
        f = open(file_name, 'r')
        for line in f:
            cols = line.split(',')
            cols[1].strip('\n')
            self.addData(int(cols[1]), int(cols[0]))
        self.mapData()



    def animate(self,i):
        xs = self.mapped_time
        ys = self.mapped_data
        self.ax1.clear()
        self.ax1.plot(xs, ys)

    def makeFigure(self):
        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)
        plt.show()


# Test Code
# s = Sensor()
# s.readData("test1.csv")
# #s.makeFigure()
# #print(len(s.values))
# print(s.mapped_data)
# print(s.mapTime())
# print(s.calc_interval())