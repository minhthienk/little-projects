#!/usr/bin/python3
from setproctitle import setproctitle
setproctitle('killpython')

import os
os.system("killall python")
os.system("killall python3")


import notify2
notify2.init('Python Killer')
n = notify2.Notification('Python Killer', 'Killed all python processes').show()
os.system("killall killpython")