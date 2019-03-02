import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))

# Windows and Linux
'''
if sys.maxsize > 2**32:
	arch_dir = '../LeapSDK/lib/x64'
else:
	arch_dir = '../LeapSDK/lib/x86'

lib_dir = os.path.abspath(os.path.join(src_dir, arch_dir))
sys.path.insert(0, lib_dir)
'''
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, lib_dir)

import Leap
