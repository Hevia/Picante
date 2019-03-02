import sys
from leap_python3 import Leap 


class SampleListener(Leap.Listener):
	
	def on_connect(self, controller):
		print("Connected")
	
	def on_frame(self, controller):
		print("Frames avaible")
		
		
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
