
from PyQt5.QtCore import QTimer, QLocale
from PyQt5.QtWidgets import QApplication, QMainWindow, QSpinBox, QSlider, QMessageBox
from PyQt5.uic import loadUi

import os
import sys
from configparser import ConfigParser

import telnetlib
import time


class MainWindow(QMainWindow):

	def __init__(self, configfile):

		super().__init__()
		loadUi(os.getcwd()+'/gqrx_sweep.ui',self)
		self.setWindowTitle('gqrx sweeper')

		### load config
		self.config = ConfigParser()
		self.config.read(configfile)
		# main
		self.debugmode = self.config.getboolean('main', 'debugmode')
		self.setLocale(QLocale(QLocale.C))  # dot as decimal separator
		# sweep
		self.centerfreq = self.config.getint('sweep', 'centerfreq')
		self.freqstep = self.config.getint('sweep', 'freqstep')

		### start Telnet TCP connection
		self.connection = False
		self.try_to_connect = True
		while self.try_to_connect:
			try:
				self.tn = telnetlib.Telnet(self.config.get('telnet', 'HOST'), self.config.getint('telnet', 'PORT'))
				self.connection = True
				self.try_to_connect = False
			except ConnectionRefusedError:
				answer = QMessageBox.question(
					self,
					"TCP connection failed", 
					'Connecting to gqrx via Telnet TCP failed.\nBefore trying again, make sure to have gqrx open, enable remote control, and make sure gqrx remote control settings match the settings in config.ini.\nYou can try again now, or close the application and restart it later.\n\nDo you want to try again now?',
					QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
					)
				if answer==QMessageBox.StandardButton.No:
					self.try_to_connect = False
					self.connection = False
					print('Operation without Telnet TCP connection. (Should be quite useless.)')

		### setup timer for sweep (triggers next step)
		self.timer = QTimer()
		self.timer.timeout.connect(self.step_up)
		self.interrupt = False

		### connect gui elements with functions
		# spinBox for center frequency
		self.spinBox_mhz.setRange(self.config.getint('sweep', 'minfreq'), self.config.getint('sweep', 'maxfreq'))
		self.spinBox_mhz.setValue(self.centerfreq)
		self.send_freq()
		self.spinBox_mhz.valueChanged.connect(self.centerfreq_changed)
		# horizontalSlider for center frequency
		self.horizontalSlider_mhz.setRange(self.config.getint('sweep', 'minfreq'), self.config.getint('sweep', 'maxfreq'))
		self.horizontalSlider_mhz.setValue(self.centerfreq)
		self.horizontalSlider_mhz.setTickPosition(QSlider.TicksBelow)
		self.horizontalSlider_mhz.setTickInterval(500)
		self.horizontalSlider_mhz.sliderReleased.connect(self.slider_released)
		# spinBoxes for sweep
		self.spinBox_start.setRange(self.config.getint('sweep', 'minfreq'), self.config.getint('sweep', 'maxfreq'))
		self.spinBox_start.setValue(self.config.getint('sweep', 'start'))
		self.spinBox_stop.setRange(self.config.getint('sweep', 'minfreq'), self.config.getint('sweep', 'maxfreq'))
		self.spinBox_stop.setValue(self.config.getint('sweep', 'stop'))
		self.doubleSpinBox_timestep.setRange(0., 60.)  # hardcoded, since a change should really be unnecessary.
		self.doubleSpinBox_timestep.setDecimals(1)
		self.doubleSpinBox_timestep.setSingleStep(0.1)
		self.doubleSpinBox_timestep.setValue(self.config.getfloat('sweep', 'timestep'))
		# PushButtons
		self.pushButton_startsweep.clicked.connect(self.sweep_start)
		self.pushButton_stopsweep.clicked.connect(self.sweep_interrupt)


	def centerfreq_changed(self):
		self.centerfreq = self.spinBox_mhz.value()
		self.horizontalSlider_mhz.setValue(self.centerfreq)
		self.send_freq()

	def slider_released(self):
		self.centerfreq = self.horizontalSlider_mhz.value()
		self.spinBox_mhz.setValue(self.centerfreq)

	def sweep_start(self):
		self.interrupt = False
		timestep_ms = int(self.doubleSpinBox_timestep.value()*1000)
		self.timer.start(timestep_ms)  # in ms - 1000 means the timer triggers once every second
		self.centerfreq = self.spinBox_start.value()

	def step_up(self):
		'Sweep through the frequency range.'
		if not self.interrupt:
			if self.centerfreq <= self.spinBox_stop.value():
				self.horizontalSlider_mhz.setValue(self.centerfreq)
				self.spinBox_mhz.setValue(self.centerfreq)
				self.centerfreq += self.freqstep
			else:
				self.timer.stop()	
		else:
			self.timer.stop()

	def sweep_interrupt(self):
		self.interrupt = True

	def send_freq(self):
		command = 'F '+str(int(self.centerfreq*1e6))+'\r\n'
		if self.debugmode: print(command)
		if self.connection: 
			self.tn.write((command.encode('ascii')))
		else:
			print('Command not send due to lacking connection.')



### open Window

configfile = 'config.ini'
with open('gqrx_sweep.qss','r') as qss:
	style = qss.read()

app = QApplication(sys.argv)
app.setStyleSheet(style)
win = MainWindow(configfile)
win.show()
sys.exit(app.exec_())