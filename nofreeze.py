#!/usr/bin/python3
from setproctitle import setproctitle
import psutil
import time
import os
import notify2

import subprocess
os.system("killall nofreeze")


setproctitle('nofreeze')

warning_flag = False
timecount = 0

time.sleep(2)

notify2.init('No Freeze')
n = notify2.Notification('No Freeze', 'Nofreeze starts')
n.show()


THRESHOLD_RAM = 2

def calculate_ram():
	return psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

# you can calculate percentage of available memory
while True:
	available_ram = calculate_ram()
	#print(available_ram)
	time.sleep(2)
	if available_ram<=10 and warning_flag==False:
		#zenipy.zenipy.message(title='No Freeze', text='WARNING: 10% available RAM', width=330, height=120, timeout=2)
		n = notify2.Notification('No Freeze', 'WARNING: 10% available RAM').show()

		warning_flag = True
		timecount=0

	if available_ram<=THRESHOLD_RAM:
		count = 0
		while True:
			if calculate_ram()<=THRESHOLD_RAM:
				count += 1
				time.sleep(1)

				if count==10:
					os.system("killall chrome")
					os.system("killall brave")
			else:
				break

	timecount+=1
	if timecount==20:
		warning_flag=False