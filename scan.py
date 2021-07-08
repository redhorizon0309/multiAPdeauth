
#!/usr/bin/env python

import sys, os, signal, re
from time import sleep
from multiprocessing import Process
from scapy.all import *

interface='' # monitor interface
aps = {} # dictionary to store unique APs

def printAP():
    with open('APs.txt','r') as aps_list:
        for line in aps_list:
            print(line,end = '')

def isAPempty():
    with open('APs.txt','r') as aps_list:
        lines = aps_list.readlines()
        if len(lines) == 0:
            return 1
        else:
            return 0

def isAPsave(bssid):
    if isAPempty():
        return 0
    else:
        with open('APs.txt','r') as aps_list:
            hit=0
            for line in aps_list:
                if re.search(bssid,line,re.I):
                    hit += 1
            if hit == 0 :
                return 0
            else :
                return 1

def storeAP(channel,encrypt,bssid,ssid):
    if isAPsave(bssid):
        return
    else:
        with open('APs.txt','a') as aps_list:
            ap = str(channel)+','+str(encrypt)+','+str(bssid)+','+str(ssid)+'\n'
            aps_list.write(ap)

def clearAP():
    with open('APs.txt','w') as aps_list:
        aps_list.truncate(0)


# process unique sniffed Beacons and ProbeResponses. 
#haslayer packet has Dot11 layer present
#ord() string to integer ex ord('a) will give 97
def sniffAP(p):
    if ( (p.haslayer(Dot11Beacon))):
        ssid       = p[Dot11Elt].info
        bssid      = p[Dot11].addr3    
        channel    = int( ord(p[Dot11Elt:3].info))
        capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                {Dot11ProbeResp:%Dot11ProbeResp.cap%}")

        # Check for encrypted networks
        if re.search("privacy", capability): encrypt = 'Y'
        else: encrypt  = 'N'

        # Display discovered AP    
        if not isAPsave(bssid):
            print("%02d  %s  %s %s" % (int(channel), encrypt, bssid, ssid))

        # Save discovered AP
        storeAP(channel,encrypt,bssid,ssid)



# Channel hopper - we are making a channel hopper because we want to scan the whole wireless spectrum.
#first choose a random channel using randrange function
#use system to run the shell command iw dev wlan0 set channel 1
#exit when a keyboard interrupt is given CTrl+c
def channel_hopper():
    channel = 1
    up = True
    while True:
        try:
            print("scanning channel %d" %(channel))
            os.system("iw dev %s set channel %d" % (interface, channel))
            time.sleep(1)
            if (channel == 15): up = False
            elif (channel == 1): up = True
            if (up == True): channel +=1
            else: channel -=1
        except KeyboardInterrupt:
            break

# Capture interrupt signal and cleanup before exiting
#terminate is used to end the child process
#before exiting the program we will be displaying number of aps found etc.
#here Cntrl+c is used to 
#signal_handler used to do clean up before the program exits

def signal_handler(signal, frame):
    p.terminate()
    p.join()

    printAP()

    #clearAP()
    sys.exit(0)


#use this for command line variables 
#for checking the number of command line variables and if they are in right order
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage %s monitor_interface" % sys.argv[0])
        sys.exit(1)

    interface = sys.argv[1]
    #take mon0 as interface given in the fist command line variable
    # Print the program header
    print("-=-=-=-=-=-= scan.py =-=-=-=-=-=-")
    print("CH ENC BSSID             SSID")

    # Start the channel hopper
    #In multiprocessing, processes are spawned by creating a Process object and then calling its start() method
    p = Process(target = channel_hopper)
    p.start()

    # Capture CTRL-C 
    #this will call the signal handler CTRL+C comes under the SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    # Start the sniffer
    sniff(iface=interface,prn=sniffAP)
    #inbuit scapy function to start sniffing calls a function which defines the criteria and we need to give the interface



