import sys
import subprocess
import os


class cd:
	"""Context manager for changing the current working directory"""
	def __init__(self, newPath):
		self.newPath = os.path.expanduser(newPath)

	def __enter__(self):
		self.savedPath = os.getcwd()
		os.chdir(self.newPath)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.savedPath)

def compile():
	curpath = os.path.dirname(__file__)
	curvepath = os.path.join(curpath, "ImageProcess/Curves/libcurves/")
	with cd(curvepath):
		subprocess.call([sys.executable, "setup.py", "build_ext", "--inplace"])

