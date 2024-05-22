
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

import os
import sys
from configparser import ConfigParser

import telnetlib
import time


connect = True  # remove later # telnetlib.Telnet 

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
		self.HOST = self.config.get('telnet', 'HOST')
		self.PORT = self.config.getint('telnet', 'PORT')
		if self.debugmode:
			print('HOST = ', self.HOST)
			print('type(HOST) = ', type(self.HOST))
			print('PORT = ', self.PORT)
			print('type(PORT) = ', type(self.PORT))
			print()			
		if connect: self.tn = telnetlib.Telnet(self.HOST, self.PORT)
		# sweep
		self.centerfreq = self.config.getint('sweep', 'centerfreq')
		self.start = self.config.getint('sweep', 'start')
		self.stop = self.config.getint('sweep', 'stop')
		self.timestep = self.config.getfloat('sweep', 'timestep')
		self.freqstep = self.config.getint('sweep', 'freqstep')
		self.keyboard_control = self.config.getboolean('sweep', 'keyboard_control')

		### connect PushButtons
		self.pushButton_startsweep.clicked.connect(self.sweep)

	def sweep(self):
		'Sweep through the frequency range.'
		freq = self.start
		while freq <= self.stop:
			command = 'F '+str(int(freq*1e6))+'\r\n'
			if self.debugmode: print(command)
			if connect: self.tn.write((command.encode('ascii')))
			freq += self.freqstep
			time.sleep(self.timestep)




### open Window

configfile = 'config.ini'
with open('gqrx_sweep.qss','r') as qss:
	style = qss.read()

app = QApplication(sys.argv)
app.setStyleSheet(style)
win = MainWindow(configfile)
win.show()
sys.exit(app.exec_())