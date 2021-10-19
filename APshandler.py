import json
import re, sys
import os.path
from multideauth import *

apid_pos = 0
ssid_pos = 1
bssid_pos = 2
channel_pos = 3
encryption_pos = 4

interface = ''
aps_list = 'APs.json'
targets_list = 'targets.json'
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
            for i in range(len(aps)):
                if aps  [i][bssid_pos] == bssid:
                    return 1
    return 0

def AP_append(fileName, bssid, ssid, channel, encryption):
    if not APs_exist(fileName):
        APs_init(fileName)

    apsList = get_APs(fileName)
    aps = apsList["aps"]
    id = str(len(aps)+1)
    ap = [id,ssid,bssid,channel,encryption]
    if not AP_exist(fileName,bssid):
        aps.append(ap)
        with open (fileName, "w+") as jsonFile :
            jsonFile.write(json.dumps(apsList))


def AP_select(apid,fileName,targetFile):
    if not APs_exist(targetFile):
        APs_init(targetFile)
    if APs_exist(fileName):
        apsList = get_APs(fileName)
        aps = apsList["aps"]
        found = False
        for i in range(len(aps)):
            if apid == aps[i][apid_pos]:
                found = True
                AP_append(targetFile,aps[i][bssid_pos],aps[i][ssid_pos],aps[i][channel_pos],aps[i][encryption_pos])
    else:
        print('[ERROR]: %s not found' %(fileName))

def AP_remove(apid,fileName):
    if APs_exist(fileName):
        apsList = get_APs(fileName)
        aps = apsList["aps"]
        found = False
        for i in range(len(aps)):
            if apid == aps[i][apid_pos]:
                found = True
                print('[Target list]: Remove AP %s' % (apid))
                del aps[i]
                with open (fileName, "w+") as jsonFile :
                    jsonFile.write(json.dumps(apsList))
                return
        if found == False : print('[ERROR]: Invalid ID')
        

def APs_show(fileName):
    if APs_exist(fileName):
        apsList = get_APs(fileName)
        aps = apsList["aps"]
        ap_table_header = "|"+"ID".ljust(3)+" | "+"Channel".ljust(8)+" | "+"BSSID".ljust(18)+" | "+"SSID".ljust(30)+" | "+"Encryption".ljust(20)+"|"
        print("_"*len(str(ap_table_header)))
        print(ap_table_header)
        for i in range(len(aps)):
            apid = str(aps[i][apid_pos]).ljust(3)
            enc = str(aps[i][encryption_pos]).ljust(20)
            c = str(aps[i][channel_pos]).ljust(8)
            bssid = str(aps[i][bssid_pos]).ljust(18)
            ssid = str(aps[i][ssid_pos]).ljust(30)
            ap_data = "|"+apid+" | "+c+" | "+bssid+" | "+ssid+" | "+enc+"|"
            print(str(ap_data))
        print("|"+"_"*(len(str(ap_table_header))-2)+"|")
        
    else:
        print('[ERROR]: %s not found' %(fileName))

def clear_AP(fileName):
    with open(fileName,'w+') as jsonFile:
        jsonFile.truncate(0)
    APs_init(fileName)

def select_target():
    apid = str(input('[APs list]: Select added AP id: '))
    AP_select(apid,aps_list,targets_list)
    target_menu(interface)

def remove_target():
    apid = str(input('[Targets list]: Select remove AP id: '))
    if re.match('^\d+$',apid):
        AP_remove(apid,targets_list)
    target_menu(interface)

def target_menu(interface):
        os.system('clear')
        print('[Scanned]:')
        APs_show(aps_list)
        print('[Selected]:')
        APs_show(targets_list)
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
            elif function == '2' :
                remove_target()
            elif function == '3' :
                clear_AP(targets_list)
                target_menu(interface)
            elif function == '4':
                try:                
                    multi_deauth(targets_list,interface,broadcast)
                except KeyboardInterrupt:
                    print('[Deauth]: Stop.')
                    target_menu(interface)
            elif function == '5':
                try:
                    client_mac = str(input('[Deauth]: Target client`s mac address: '))
                    if is_mac(client_mac):
                        multi_deauth(targets_list,interface,client_mac)
                    else:
                        print('[ERROR]: Invalid client`s address.')
                        time.sleep(1)
                except KeyboardInterrupt:
                    target_menu(interface)
            elif function == '6' :
                sys.exit(0)
            else:
                print('[ERROR]: Invalid Input')
