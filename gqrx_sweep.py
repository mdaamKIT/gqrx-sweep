
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

import os
import sys
from configparser import ConfigParser

import telnetlib
import time


connect = True  # remove later # telnetlib.Telnet returns ConnetctionRefusedError, if nobody listens. (Could also use try/except.)

class MainWindow(QMainWindow):

	def __init__(self, configfile):
		super().__init__()
		loadUi(os.getcwd()+'/gqrx_sweep.ui',self)

		### load config
		self.config = ConfigParser()
		self.config.read(configfile)
		# main
		self.debugmode = self.config.getboolean('main', 'debugmode')
		# telnet		
		if connect: self.tn = telnetlib.Telnet(self.config.get('telnet', 'HOST'), self.config.getint('telnet', 'PORT'))
		# sweep
		self.centerfreq = self.config.getint('sweep', 'centerfreq')
		self.start = self.config.getint('sweep', 'start')
		self.stop = self.config.getint('sweep', 'stop')
		self.timestep = self.config.getfloat('sweep', 'timestep')
		self.freqstep = self.config.getint('sweep', 'freqstep')
		self.keyboard_control = self.config.getboolean('sweep', 'keyboard_control')

		### connect PushButtons
		self.pushButton_startsweep.clicked.connect(self.sweep_start)
		self.pushButton_stopsweep.clicked.connect(self.sweep_interrupt)

		### setup the sweep 
		self.timer = QTimer() # timer to trigger next step (sweep)
		self.timer.timeout.connect(self.step_up)
		self.interrupt = False

	def sweep_start(self):
		self.interrupt = False
		timestep_ms = int(self.timestep*1000)
		self.timer.start(timestep_ms)  # in ms - 1000 means the timer triggers once every second
		self.freq = self.start

	def step_up(self):
		'Sweep through the frequency range.'
		if not self.interrupt:
			if self.freq <= self.stop:
				self.send_freq()
				self.freq += self.freqstep
			else:
				self.timer.stop()	
		else:
			self.timer.stop()

	def sweep_interrupt(self):
		self.interrupt = True

	def send_freq(self):
		command = 'F '+str(int(self.freq*1e6))+'\r\n'
		if self.debugmode: print(command)
		if connect: self.tn.write((command.encode('ascii')))




### open Window

configfile = 'config.ini'
with open('gqrx_sweep.qss','r') as qss:
	style = qss.read()

app = QApplication(sys.argv)
app.setStyleSheet(style)
win = MainWindow(configfile)
win.show()
sys.exit(app.exec_())