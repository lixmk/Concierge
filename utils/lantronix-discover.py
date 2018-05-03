#!/usr/bin/env python
# By Mike Kelly
# exfil.co
# @lixmk
#
# This script is part of the Concierge Toolkit
# https://github.com/lixmk/Concierge
#

import socket
import argparse
import netaddr
import re
import sys
from time import sleep
from os import path
from os import geteuid

# Discover PACGDX 512IP Door Controllers
def lantronix_discover_udp():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setblocking(0)
    pkt0 = '000000f6'.decode('hex')
    s.sendto(pkt0, (str(ip), 30718))
    s.settimeout(.5)
    rsp = s.recv(1024)
    if "000000f7" in rsp.encode('hex')[:8]:
        #mac = rsp.encode('hex')[50:]
        mac = ':'.join(rsp.encode('hex')[50:][i:i+2] for i in range(0, len(rsp.encode('hex')[50:]), 2))
        print "[+] Lantronix module discovered"
        print "[+]     IP Addr: "+str(ip)
        print "[+]     MAC Addr: "+mac
        with open("lantronix-details.csv","a+")as f:
            f.write(str(ip)+","+mac+"\n")
    s.close

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='./lantronix-discover.py -r 10.0.0.1/24 -v')
    parser.add_argument('-r', '--rhosts', required=True, help='Target CIDR Range')
    args = parser.parse_args()
    rhosts = args.rhosts
    print "###############################################"
    print "#              Concierge Toolkit              #"
    print "#                                             #"
    print "# Lantronix Serial to TCP/IP Module Discovery #"
    print "###############################################"
    print ""
    try:
        if not geteuid() == 0:
            print "[!] This script must be run with root privileges."
            sys.exit()
        print "[*] Starting door controller discovery."
        if path.isfile("lantronix-details.csv") == 0:
            with open("lantronix-details.csv","a+")as f:
                f.write("rhost,mac addr\n")
        for ip in netaddr.IPNetwork(rhosts).iter_hosts():
            lantronix_discover_udp()
    except (KeyboardInterrupt, SystemExit)as e:
        print ""
        print "Keyboard Interrupt: Stopping all processes"
        sys.exit()
    except (socket.timeout, socket.error):
        pass
    except (IndexError):
        pass
    print "[*] Lantronix module discovery of "+rhosts+" complete."
