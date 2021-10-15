#!/usr/bin/env python
import os

def monitor_up(interface):
    print('[Interface]: %s monitor mode up' % (interface))
    os.system("sudo airmon-ng start %s" % (str(interface)))
    interface = str(interface+'mon') 
    return interface

def monitor_down(interface):
    print('[Interface]: %s monitor mode down' % (interface))
    os.system("sudo airmon-ng stop %s" % (str(interface)))
    interface = str(interface).strip('mon')
    return interface