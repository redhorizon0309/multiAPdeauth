import json
import re, sys
import os.path
from multideauth import *
from monitormode import *

signal_strength_pos = 0
ssid_pos = 1
bssid_pos = 2
channel_pos = 3
encryption_pos = 4
select_pos = 5
interface = ''
aps_list = 'APs.json'
broadcast = 'FF:FF:FF:FF:FF:FF'

#AP handler
def padding(length, text):
    for i in range(0,length):
        if text[i] == "" :
            text = text+" "

def is_mac(address):
    mac_pattern = re.compile(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})') 
    if mac_pattern.match(address):
        return 1
    else:
        return 0

def APs_exist(fileName):
    if os.path.exists(fileName):
        return 1
    else:
        return 0

def APs_init(fileName):
    apsList = {"aps":[]}
    with open (fileName, "w+") as jsonFile :
        jsonFile.write(json.dumps(apsList))

def get_APs(fileName):
    if APs_exist(fileName):
        apsList = open(fileName,"r+")
        aps_data = json.load(apsList)
        apsList.close()
        return aps_data

def AP_exist(fileName, bssid):
    if APs_exist(fileName):
        apsList = get_APs(fileName)
        aps = apsList["aps"]
        if len(aps) != 0:
            for apid in range(len(aps)):
                if aps[apid][bssid_pos] == bssid:
                    return 1
    return 0

def AP_append(fileName, bssid, ssid, channel, encryption, strength):
    if not APs_exist(fileName):
        APs_init(fileName)

    apsList = get_APs(fileName)
    aps = apsList["aps"]
    select = False
    ap = [strength,ssid,bssid,channel,encryption,select]
    if not AP_exist(fileName,bssid):
        aps.append(ap)
        with open (fileName, "w+") as jsonFile :
            jsonFile.write(json.dumps(apsList))

def update_strength(fileName, strength, bssid):
    if APs_exist(fileName):
        apsList = get_APs(fileName)
        aps = apsList["aps"]
        for apid in range(len(aps)):
            if aps[apid][bssid_pos] == bssid:
                if aps[apid][signal_strength_pos] != strength:
                    aps[apid][signal_strength_pos] = strength
                    with open (fileName, "w+") as jsonFile :
                        jsonFile.write(json.dumps(apsList))
    else:
        print('[ERROR]: %s not found' %(fileName))

def AP_select(apid,fileName):
    if APs_exist(fileName):
        apsList = get_APs(fileName)
        aps = apsList["aps"]
        if apid in range(len(aps)):
            aps[apid][select_pos] = True
            with open (fileName, "w+") as jsonFile :
                jsonFile.write(json.dumps(apsList))
        else: print('[ERROR]: Invalid ID')
    else:
        print('[ERROR]: %s not found' %(fileName))

def AP_remove(apid,fileName):
    if APs_exist(fileName):
        apsList = get_APs(fileName)
        aps = apsList["aps"]
        if apid in range(len(aps)):
            aps[apid][select_pos] = False
            with open (fileName, "w+") as jsonFile :
                jsonFile.write(json.dumps(apsList))
        else: print('[ERROR]: Invalid ID')
    else:
        print('[ERROR]: %s not found' %(fileName))

        

def APs_show(fileName):
    if APs_exist(fileName):
        apsList = get_APs(fileName)
        aps = apsList["aps"]
        ap_table_header = "|"+"ID".ljust(3)+" | "+"Signal".ljust(7)+" | "+"Channel".ljust(8)+" | "+"BSSID".ljust(18)+" | "+"SSID".ljust(30)+" | "+"Encryption".ljust(20)+" | |"
        print("_"*len(str(ap_table_header)))
        print(ap_table_header)
        for i in range(len(aps)):
            apid = str(aps[i][signal_strength_pos]).ljust(7)
            enc = str(aps[i][encryption_pos]).ljust(20)
            c = str(aps[i][channel_pos]).ljust(8)
            bssid = str(aps[i][bssid_pos]).ljust(18)
            ssid = str(aps[i][ssid_pos]).ljust(30)
            if aps[i][select_pos] == True:
                select = " |X"
            elif aps[i][select_pos] == False: 
                select = " |O"
            ap_data = "|"+str(i+1).ljust(3)+" | "+apid+" | "+c+" | "+bssid+" | "+ssid+" | "+enc+select+"|"
            print(str(ap_data))
        print("|"+"_"*3+"_|_"+"_"*7+"_|_"+"_"*8+"_|_"+"_"*18+"_|_"+"_"*30+"_|_"+"_"*20+"_|_|")
        
    else:
        print('[ERROR]: %s not found' %(fileName))

def clear_AP(fileName):
    with open(fileName,'w+') as jsonFile:
        jsonFile.truncate(0)
    APs_init(fileName)

def select_target():
    apid = int(input('[APs list]: Select added AP id: '))-1
    AP_select(apid,aps_list)

def remove_target():
    apid = int(input('[Targets list]: Select remove AP id: '))-1
    AP_remove(apid,aps_list)

def target_menu(interface):
    os.system('clear')
    print('[Interface]: %s' %(interface))
    print('[Scanned]:')
    APs_show(aps_list)
    print('[Function]:')
    print('[1]: Select target')
    print('[2]: Remove target')
    print('[3]: Clear targets')
    print('[4]: Broadcast deauth')
    print('[5]: Deauth single client')
    print('[6]: Exit')
    function = input('[Function]: ')
    if not re.match('^[1-6]$',function):
        print('[ERROR]: Invalid Input')
    else:
        if function == '1' :
            select_target()
            target_menu(interface)
        elif function == '2' :
            remove_target()
            target_menu(interface)
        elif function == '3' :
            clear_AP(aps_list)
            target_menu(interface)
        elif function == '4':
            try:
                interface = monitor_up(interface)
                print('[Interface]: Deauth on %s' %(interface))
                multi_deauth(aps_list,interface,broadcast)
            except KeyboardInterrupt:
                interface = monitor_down(interface)
                print('[Deauth]: Stop.')
                target_menu(interface)
        elif function == '5':
            try:
                client_mac = str(input('[Deauth]: Target client`s mac address: '))
                if is_mac(client_mac):
                    multi_deauth(aps_list,interface,client_mac)
                else:
                    print('[ERROR]: Invalid client`s address.')
                    time.sleep(1)
            except KeyboardInterrupt:
                target_menu(interface)
        elif function == '6' :
            sys.exit(0)
        else:
            print('[ERROR]: Invalid Input')

if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            print("[Usage]: %s [mode] [apid]" % sys.argv[0])
            print("[Usage]: mode 1 = add; mode 2 = remove")
            sys.exit(1)

        mode = int(sys.argv[1])
        apid = int(sys.argv[2])-1
        print(mode)
        if mode == 1:
            AP_select(apid,aps_list)
        elif mode == 2:
            AP_remove(apid,aps_list)
    except:
        print('[ERROR]: Invalid Input')