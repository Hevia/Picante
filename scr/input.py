import glob
import serial
import sys
import leap_input
import time

#leap_input.get_input()
f = open("output.txt", "w")

def panic():
	print("Oh shit, everything is broken in Serial Land")


class Communication_Device:
	
	def __init__(self, InType=None, Port=0, BitRate=0, NumSensors=0):
		
		# What type of input are we dealing with (Serial, Socket, etc)
		if InType is None:
			#self.InType, self.Port = ('COM', self.listSerialPorts()[0]) # assume the first port is Arduino
			if sys.platform.startswith('win'):
				self.InType = 'COM'
				self.Port = 'COM3'
			else:
				self.InType = 'tty*'
				self.Port = '/dev/ttyACM0'
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
			try:
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
				#if time.time() > timeout:
					#break
			except KeyboardInterrupt:
				print("Keyboard Interrupt")
				break

		if not sys.platform.startswith('win'):
			self.leap[0].remove_listener(self.leap[1])

	if sys.platform.startswith('win'):
		def process_frame(self, frame):

			data = {};
			if frame is "Invalid Frame":
				return None

			#print("Hands: {0}, fingers {1}".format(len(frame), (len(frame[0].fingers)+len(frame[0].fingers))))
			i = 0;
			for h in frame:
				pos = (h.palm_normal.x, h.palm_normal.y, h.palm_normal.z)
				vel = (h.palm_velocity.x,h.palm_velocity.y,h.palm_velocity.z)
				values = pos, vel
				data[i] = pos
				data[i+1] = vel
				print(values)
				#for finger in h.fingers:
					#print(finger.type)
					#for bone in finger.bones:
						#print(bone.type)
				i+=2
			return data
	else:
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
				normal = hand.palm_normal
				direction = hand.direction

				# Calculate the hand's pitch, roll and yaw angles
				print("   pitch: {0} degrees, roll: {1} degrees, yaw: {2} degrees".format(direction.pitch * Leap.RAD_TO_DEG, normal.roll * Leap.RAD_TO_DEG, direction.yaw * Leap.RAD_TO_DEG))
				handData.append((direction.pitch * Leap.RAD_TO_DEG, normal.roll * Leap.RAD_TO_DEG, direction.yaw * Leap.RAD_TO_DEG))

				# Get fingers
				for finger in hand.fingers:
					print("     {0} finger, id {1}, lenght: {2}mm, width {3}mm".format(self.finger_names[finger.type], finger.id, finger.length, finger.width))

				data[handType] = handData
				# Get the hand's normal vector and direction

			return data
		
	def log_data(self, leap_data, ardin_data):
		if not ardin_data or not leap_data:
			return
		if len(ardin_data) == 1:
			return


		f.write("{0}, ".format(ardin_data))
		for key in leap_data.keys():
			f.write("{0}, ".format(leap_data[key]))
		f.write("\n")

c = Communication_Device()
c.read_data_stream()
