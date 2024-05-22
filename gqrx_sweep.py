
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

import os
import sys
from configparser import ConfigParser


class MainWindow(QMainWindow):

	def __init__(self, start, stop, timestep, freqstep, keyboard_control):
		super().__init__()
		loadUi(os.getcwd()+'/gqrx_sweep.ui',self)
		self.start = start
		self.stop = stop
		self.timestep = timestep
		self.freqstep = freqstep
		self.keyboard_control = keyboard_control


# open Window
# -----------

config = ConfigParser()
config.read('config.ini')
start = config.get('main', 'start')
stop = config.get('main', 'stop')
timestep = config.get('main', 'timestep')
freqstep = config.get('main', 'freqstep')
keyboard_control = config.get('main', 'keyboard_control')

with open('gqrx_sweep.qss','r') as qss:
	style = qss.read()

app = QApplication(sys.argv)
app.setStyleSheet(style)
win = MainWindow(start, stop, timestep, freqstep, keyboard_control)
win.show()
sys.exit(app.exec_())