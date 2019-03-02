import glob
import serial
import sys
import leap_input

#leap_input.get_input()

def panic():
	print("Oh shit, everything is broken in Serial Land")


class Communication_Device:
	
	def __init__(self, InType=None, Port=0, BitRate=0, NumSensors=0):
		
		# What type of input are we dealing with (Serial, Socket, etc)
		if InType is None:
			self.InType, self.Port = ('COM', self.listSerialPorts()[0]) # assume the first port is Arduino 
		else:
			self.InType = InType
			self.Port = Port
			
		# Create the Arduino member
		try:
			self.arduino = serial.Serial(self.Port)
			self.leap = self.__initLeap() # SEG FAULT HERE
		except (OSError, serial.SerialException):
			panic()
			
		
	def __initLeap(self):
		return leap_input.create_controller()
	
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
				print(s)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass
		return result
		
	def read_data_stream(self):
		while True:
			print(self.leap[0].frame())
			arduino_data = self.arduino.readline()[:-2].decode("utf-8")
			if arduino_data:
				print(arduino_data)
		self.leap[0].remove_listener(self.leap[1])

c = Communication_Device()
c.read_data_stream()
