#!/usr/bin/env python

import sys, os, signal, re
import xml.etree.ElementTree as ET
from time import sleep
from multiprocessing import Process
from scapy.all import *

aps_list = 'APs.xml'
interface = '' # monitor interface
aps = {} # dictionary to store unique APs

def monitor_up(interface):
    os.system("sudo airmon-ng start %s" % (str(interface)))
    interface = str(interface+'mon') 
    return interface

def monitor_down(interface):
    #print("turn %s to station mode" % (str(interface)))
    os.system("sudo airmon-ng stop %s" % (str(interface)))

#AP handler
def padding(length, text):
    for i in range(0,length):
        if text[i] == "" :
            text = text+" "
             
def APs_init(fileName):
    aps = ET.Element('AccessPoints')
    apsList = ET.ElementTree(aps)
    with open (fileName, "wb") as files :
        apsList.write(files)

def AP_exist(fileName, bssid):
    apsList = ET.parse(fileName)
    aps = apsList.getroot()

    for ap in aps.findall('AccessPoint'):
        if ap.findtext('BSSID') == bssid:
            return 1
    return 0

def AP_append(fileName, bssid, ssid, channel, encryption):
    apsList = ET.parse(fileName)
    aps = apsList.getroot()

    if not AP_exist(fileName, bssid):
        ap = ET.Element("AccessPoint")
        ap.set("Channel",channel)
        ap.set("Encryption",encryption)
        apBssid = ET.SubElement(ap,"BSSID")
        apBssid.text = bssid
        apSsid = ET.SubElement(ap,"SSID")
        apSsid.text = ssid
        aps.append(ap)
        apsList.write(fileName)

def APs_show(fileName):
    apsList = ET.parse(fileName)
    aps = apsList.getroot()

    ap_table_header = "|"+"Encryption".ljust(10)+" | "+"Channel".ljust(8)+" | "+"BSSID".ljust(18)+" | "+"SSID".ljust(20)+"|"
    print("_"*len(str(ap_table_header)))
    print(ap_table_header)
    for ap in aps.findall('AccessPoint'):
        enc = str(ap.get('Encryption')).ljust(10)
        c = str(ap.get('Channel')).ljust(8)
        bssid = str(ap.findtext('BSSID')).ljust(18)
        ssid = str(ap.findtext('SSID')).ljust(20)
        ap_data = "|"+enc+" | "+c+" | "+bssid+" | "+ssid+"|"
        print(str(ap_data))
        
    print("-"*len(str(ap_table_header)))

def clearAP():
    with open(aps_list,'w') as aps_list:
        aps_list.truncate(0)


# process unique sniffed Beacons and ProbeResponses. 
#haslayer packet has Dot11 layer present
#ord() string to integer ex ord('a) will give 97
def sniffAP(p):
    if ( (p.haslayer(Dot11Beacon))):
        ssid       = str(p[Dot11Elt].info, 'utf-8')
        bssid      = p[Dot11].addr3    
        channel    = int( ord(p[Dot11Elt:3].info))
        capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                {Dot11ProbeResp:%Dot11ProbeResp.cap%}")

        # Check for encrypted networks
        if re.search("privacy", capability): encrypt = 'Y'
        else: encrypt  = 'N'

        # Display discovered AP    
        if not AP_exist(aps_list,bssid):
            print("[AP found]: %02d  %s  %s %s" % (int(channel), encrypt, bssid, ssid))

        # Save discovered AP
        AP_append("APs.xml", str(bssid), str(ssid), str(channel), str(encrypt))



# Channel hopper - we are making a channel hopper because we want to scan the whole wireless spectrum.
#first choose a random channel using randrange function
#use system to run the shell command iw dev wlan0 set channel 1
#exit when a keyboard interrupt is given CTrl+c
def channel_hopper():
    channel = 1
    up = True
    while True:
        try:
            print("[Scanning]: channel %d" %(channel))
            os.system("iw dev %s set channel %d" % (interface, channel))
            time.sleep(1)
            if (channel == 13): up = False
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
    
    monitor_down(interface)

    os.system('clear')
    APs_show(aps_list)
    
    sys.exit(0)


#use this for command line variables 
#for checking the number of command line variables and if they are in right order
if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("[Usage]: %s monitor_interface" % sys.argv[0])
            sys.exit(1)

        #take mon0 as interface given in the fist command line variable
        interface = sys.argv[1]

        # Change network adapter to monitor mode
        interface = monitor_up(interface)
        print("[Interface]: %s" % interface)

        # Accesspoint list init
        APs_init(aps_list)
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
    except KeyboardInterrupt:
        print("[Interupt]")

