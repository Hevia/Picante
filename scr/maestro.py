from Sensor import *
from input import *
import threading


def main():
	s = Sensor()
	c = Communication_Device()
	
	inThread = threading.Thread(target=c.read_data_stream, args=())
	outThread = threading.Thread(target=s.output_data, args=("output.txt", "fancy-out.txt"))# s.output_data("output.txt", "fancy-out.txt")
	inThread.start()
	outThread.start()
	
main()
