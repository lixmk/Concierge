#!/usr/bin/env python
# By Mike Kelly
# exfil.co
# @lixmk
#
# This script is part of the Concierge Toolkit
# https://github.com/lixmk/Concierge
#
# Uses SNMP to discover Mercury Security door controllers
# Mercury controllers (hardware and/or firmware) are rebranded by several other vendors.
# No brand parsing is done outside of the device provided information.
#

import argparse
import netaddr
import sys
from easysnmp import snmp_get
from os import path

def pulloid(ip):
    global counter
    counter = 0
    desc = str(snmp_get('iso.3.6.1.2.1.1.1.0', hostname=str(ip), community='public', version=2)).split("'")[1]
    if "Firmware Version" in desc and "Build" in desc:
        fwv = desc.replace("Version ", "Version:").replace(" Build ", ":Build:").split(':')[1]
        bnum = desc.replace("Version ", "Version:").replace(" Build ", ":Build:").split(':')[3]
        model = str(snmp_get('iso.3.6.1.2.1.1.5.0', hostname=str(ip), community='public', version=2)).split("'")[1].replace(" (contains binary)", "")
        with open("ep-snmp-details.csv","a+")as f:
            f.write(str(ip)+","+model+","+fwv+","+bnum+","+desc+"\n")
        print '[+] Found "'+model+'" Mercury OEM at '+str(ip)
        counter += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='./ep-discover-snmp.py -r 10.0.0.1/24')
    parser.add_argument('-r', '--cidr', required=True, help='Target IP address or CIDR range')
    args = parser.parse_args()
    cidr = args.cidr
    
    print "#############################################"
    print "#             Concierge Toolkit             #"
    print "#                                           #"
    print "#   Mercury OEM Controller SNMP Discovery   #"
    print "#############################################"
    print ""
    print "[*] Starting door controller discovery."

    if path.isfile("ep-snmp-details.csv") == 0:
        with open("ep-snmp-details.csv","a+")as f:
            f.write("rhost,model name,firmware version,build number,full description\n")
    for ip in netaddr.IPNetwork(cidr).iter_hosts():
        try:
            pulloid(ip)
        except (KeyboardInterrupt, SystemExit)as e:
            print "Keyboard Interrupt: Stopping all processes"
            sys.exit()
        except (IndexError):
            pass
    
    print ""
    print "[*] Mercury OEM discovery of "+cidr+" complete."
    print "[*] "+str(counter)+" device(s) discovered."


