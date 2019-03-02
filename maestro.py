import glob
import serial
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import math

style.use('fivethirtyeight')


def panic():
    print("Oh shit, everything is broken in Serial Land")




class Communication_Device:

    def __init__(self, InType=None, Port=0, BitRate=0, NumSensors=0):

        # What type of input are we dealing with (Serial, Socket, etc)
        if InType is None:
            self.InType, self.Port = ('COM', self.listSerialPorts()[0])  # assume the first port is Arduino
        else:
            self.InType = InType
            self.Port = Port

        # Create the Arduino member
        try:
            self.arduino = serial.Serial(self.Port)  # , baudrate=115200, timeout=0.1) # Port, Baud-Rate, Timeout
        except (OSError, serial.SerialException):
            panic()

    def listSerialPorts(self):
        # http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
            print(ports)

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                print("Could not open {0}".format(port))
        return result

    def read_data_stream(self):
        while True:
            data = self.arduino.readline()[:-2].decode("utf-8")
            if data:
                print(data)





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


s = Sensor()
s.addData(3295, 512)
s.addData(3347, 511)
s.addData(3553, 512)
s.makeFigure();




#c = Communication_Device()
#c.read_data_stream()

