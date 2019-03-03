from Sensor import *


def main():
	s = Sensor()
	while True:
		try:
			s.output_data("output.txt", "fancy-out.txt")
		except:
			pass
	
main()
