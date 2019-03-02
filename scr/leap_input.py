import sys
from leap_python3 import Leap 


class SampleListener(Leap.Listener):
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	
	def on_connect(self, controller):
		print("Connected")
	
	def on_frame(self, controller):
		frame = controller.frame()
		
		print("Frame id: {0}, timestamp {1}, hands: {2}, fingers {3}".format(frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))
		
		# Get hands
		for hand in frame.hands:
			handType = "Left hand" if hand.is_left else "Right hand"
			
			print("   {0}, id {1}, position: {0}".format(handType, hand.id, hand.palm_position))
			
			# Get the hand's normal vector and direction
			normal = hand.palm_normal
			direction = hand.direction
			
			# Calculate the hand's pitch, roll and yaw angles
			print("   pitch: {0} degrees, roll: {1} degrees, yaw: {2} degrees".format(direction.pitch * Leap.RAD_TO_DEG, normal.roll * Leap.RAD_TO_DEG, direction.yaw * Leap.RAD_TO_DEG))
			
			'''
			# Get arm bone
			arm = hand.arm
			print(" Arm direction: {0}, wrist position: {1}, elbow position: {2}".format(arm.direction, arm.writst_position, arm.elbow_position))
			'''
			
			# Get fingers
			for finger in hand.fingers:
				print("     {0} finger, id {1}, lenght: {2}mm, width {3}mm".format(self.finger_names[finger.type], finger.id, finger.length, finger.width))
		
		
def main():
	listener = SampleListener()
	controller = Leap.Controller()
	
	controller.add_listener(listener)
	
	# Keep this process running until Enter is Pressed
	print("Press Enter to Quit")
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)
		
main()
