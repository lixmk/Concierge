#!/usr/bin/env python
# By Mike Kelly
# exfil.co
# @lixmk
#
# This script is part of the Concierge Toolkit
# https://github.com/lixmk/Concierge
#
# Discover HID EVO and AMAG EN Series door controllers in a cidr range
#

import socket
import argparse
import SimpleHTTPServer
import SocketServer
import threading
import netaddr
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
            with open("hidevo-details.csv","a+")as f:
                f.write(str(ip)+","+rspn.split(";")[6]+","+rspn.split(";")[3]+","+rspn.split(";")[4]+","+rspn.split(";")[2]+","+rspn.split(";")[7]+","+rspn.split(";")[8]+"\n")
            # Printing to screen
            print "[+] HID EVO response received from: "+str(ip)
            print "    Device Type: "+rspn.split(";")[6]
            print "    Hostname: "+rspn.split(";")[3]
            print "    Internal IP: "+rspn.split(";")[4]
            print "    MAC Address: "+rspn.split(";")[2]
            print "    Firmware Version: "+rspn.split(";")[7]
            print "    Build Date: "+rspn.split(";")[8]
    except (KeyboardInterrupt, SystemExit):
        s.close
        print "Keyboard Interrupt: Stopping all processes"
        raise
    except (socket.timeout, socket.error):
        s.close

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='./concierge.py -a discover -r 10.0.0.1/24')
    parser.add_argument('-r', '--cidr', required=True, help='Target CIDR Range')
    args = parser.parse_args()
    cidr = args.cidr
  
    print "########################################"
    print "# Concierge: Access Control Exploition #"
    print "########################################"
    print ""
    print "[*] Starting door controller discovery."
    # Creating csv if not already there
    if path.isfile("hidevo-details.csv") == 0:
        with open("hidevo-details.csv","a+")as f:
            f.write("rhost,device type,hostname,reported ip,mac address,firmware version,build date\n")
    # Cylcling discovery through cidr range
    for ip in netaddr.IPNetwork(cidr).iter_hosts():
        try:
            hid_evo_discover()
        except (KeyboardInterrupt, SystemExit):
            print "Keyboard Interrupt: Stopping all processes"
            raise
    print "[*] HID EVO discovery of "+cidr+" complete."
