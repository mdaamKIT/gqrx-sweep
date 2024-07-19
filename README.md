# gqrx-sweep

Small GUI control panel for remote control of Gqrx (https://www.gqrx.dk/) for fast sweeps through the spectrum.
(That might be helpful, if you plan to abuse Gqrx for spectrum analysis instead of software radio stuff.)

Gqrx-sweep controls Gqrx's frequency by sending commands via telnet.


## Short user manual

1. Open Gqrx as you normally would.
2. Enable 'Remote control via TCP' by clicking the icon with the two PCs in the main toolbar. (The main toolbar toggles with 'ctrl'+'T')
3. 'Configure remote control settings' by clicking the icon with the tools in the main toolbar. Make sure Gqrx's remote control settings (port, host) match gqrx-sweep's configuration in the config.ini . By default, the port is 7356 and the host is 127.0.0.1 .
4. Open gqrx\_sweep.py with python. ('python gqrx\_sweep.py') A small GUI should open where you can enter the frequency of your choice.
5. You can set a frequency by entering the number or using the slider, and you can use the 'frequency sweep' function to automatically sweep through the spectrum.


## Dependencies

gqrx-sweep is a Python application based on PyQt5 for the GUI.
- You need the Python package pyqt5 installed.
- The other packages should already be installed with a standard installation: os, sys, configparser, telnetlib, time
