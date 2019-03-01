import glob
import serial
import sys

class Communication_Device:
	
	def __init__(self, InType=None, Port=0, BitRate=0, NumSensors=0):
		
		# What type of input are we dealing with (Serial, Socket, etc)
		if InType is None:
			print(self.listSerialPorts())
			
		self.InType = InType
	
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


c = Communication_Device()
