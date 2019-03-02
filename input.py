import glob
import serial
import sys

def panic():
	print("Oh shit, everything is broken in Serial Land")


class Communication_Device:
	
	def __init__(self, InType=None, Port=0, BitRate=0, NumSensors=0):
		
		# What type of input are we dealing with (Serial, Socket, etc)
		if InType is None:
			print(self.listSerialPorts())#self.InType, self.Port = ('COM', self.listSerialPorts()[0]) # assume the first port is Arduino 
		else:
			self.InType = InType
			self.Port = Port
			
		# Create the Arduino member
		try:
			self.arduino = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=0.1) # Port, Baud-Rate, Timeout
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

c = Communication_Device()
c.read_data_stream()
