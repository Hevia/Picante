import glob
import serial
import sys
import leap_input
import time

#leap_input.get_input()
f = open("output.txt", "a")

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
		timeout = time.time() + 60*0.30 # Read data for 30 seconds

		while True:
			if sys.platform.startswith('win'):
				leap_data = self.process_frame(self.leap.frame())
			else:
				leap_data = self.process_frame(self.leap[0].frame())

			if leap_data:
				print(leap_data)
			arduino_data = self.arduino.readline()[:-2].decode("utf-8")
			if arduino_data:
				print(arduino_data)
			
			self.log_data(leap_data, arduino_data)
			if time.time() > timeout:
				break

		if not sys.platform.startswith('win'):
			self.leap[0].remove_listener(self.leap[1])

	def process_frame(self, frame):
		
		if frame is "Invalid Frame":
			return None
		
		data = {}
		print("Frame id: {0}, timestamp {1}, hands: {2}, fingers {3}".format(frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))

		# Get hands
		for hand in frame.hands:
			handData = []
			handType = "LH" if hand.is_left else "RH"
			print("   {0}, id {1}, position: {0}".format(handType, hand.id, hand.palm_position))
			handData.append(hand.palm_position)
			# Get the hand's normal vector and direction
			normal = hand.palm_normal
			direction = hand.direction

			# Calculate the hand's pitch, roll and yaw angles
			print("   pitch: {0} degrees, roll: {1} degrees, yaw: {2} degrees".format(direction.pitch * Leap.RAD_TO_DEG, normal.roll * Leap.RAD_TO_DEG, direction.yaw * Leap.RAD_TO_DEG))
			handData.append((direction.pitch * Leap.RAD_TO_DEG, normal.roll * Leap.RAD_TO_DEG, direction.yaw * Leap.RAD_TO_DEG))

			# Get fingers
			for finger in hand.fingers:
				print("     {0} finger, id {1}, lenght: {2}mm, width {3}mm".format(self.finger_names[finger.type], finger.id, finger.length, finger.width))
			
			data[handType] = handData
			
		return data
		
	def log_data(self, leap_data, ardin_data):
		f.write("{0}, {1}".format(ardin_data, leap_data))
		
c = Communication_Device()
c.read_data_stream()
