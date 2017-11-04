#!/usr/bin/env python
# By Mike Kelly
# exfil.co
# @lixmk
#
# This script is part of the Concierge Toolkit
# https://github.com/lixmk/Concierge
#
# Used HID's discoveryd service to identify HID EVO door controllers in a cidr range.
#

import socket
import argparse
import netaddr
import sys
from time import sleep
from os import remove
from os import path

# Discovery HID Door Controllers
def hid_evo_discover():
    try:
        # Creating socket
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.setblocking(0)
        # Sending discover command
        pkt0 = "discover;013;"
        s.sendto(pkt0, (str(ip), 4070))
        s.settimeout(0.5)
        # Parsing response
        rspn = s.recv(1024)
        s.close
        # Writing response to csv
        if rspn.split(";")[0] == "discovered":
            with open("hid-evo-details.csv","a+")as f:
                f.write(str(ip)+","+rspn.split(";")[6]+","+rspn.split(";")[3]+","+rspn.split(";")[4]+","+rspn.split(";")[2]+","+rspn.split(";")[7]+","+rspn.split(";")[8]+"\n")
            # Printing to screen
            print "[+] HID EVO response received from: "+str(ip)
            print "    Device Type: "+rspn.split(";")[6]
            print "    Hostname: "+rspn.split(";")[3]
            print "    Internal IP: "+rspn.split(";")[4]
            print "    MAC Address: "+rspn.split(";")[2]
            print "    Firmware Version: "+rspn.split(";")[7]
            print "    Build Date: "+rspn.split(";")[8]
    except (socket.timeout, socket.error):
        s.close

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='./hid-evo-discover.py -r 10.0.0.1/24')
    parser.add_argument('-r', '--rhosts', required=True, help='Target CIDR Range')
    args = parser.parse_args()
    rhosts = args.rhosts
    try:
        print "#############################################"
        print "#             Concierge Toolkit             #"
        print "#                                           #"
        print "#     HID EVO door controller discovery     #"
        print "#############################################"
        print ""
        print "[!] This script is slow. The preferred method of discovery is using the nmap .nse in `utils/nse/`."
        print ""
        sleep(5)
        print "[*] Starting HID EVO door controller discovery."
        # Creating csv if not already there
        if path.isfile("hid-evo-details.csv") == 0:
            with open("hid-evo-details.csv","a+")as f:
                f.write("rhost,device type,hostname,reported ip,mac address,firmware version,build date\n")
        # Cylcling discovery through cidr range
        for ip in netaddr.IPNetwork(rhosts).iter_hosts():
            hid_evo_discover()
    except (KeyboardInterrupt, SystemExit):
        print ""
        print "[!] Keyboard Interrupt: Stopping all processes"
        sys.exit()
    print "[*] HID EVO discovery of "+rhosts+" complete."
