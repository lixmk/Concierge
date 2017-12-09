#!/usr/bin/env python
# By Mike Kelly
# exfil.co
# @lixmk
#
# This script is part of the Concierge Toolkit
# https://github.com/lixmk/Concierge
#
# Tests AMAG EN Series door controllers for CVE-2017-16241 vulnerability. This check has not been thoroughly tested for false positive/negatives
# Identified controllers are saved to endbc-CVE_2017_16241.csv
#

import socket
import argparse
import netaddr
import re
import sys
from time import sleep
from os import path

def amag_endbc_vulncheck():
    s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    pkt1 = '0230315a5a235666304439'.decode('hex')
    s2.setblocking(0)
    s2.settimeout(0.5)
    s2.connect((str(ip), 3001))
    s2.send(pkt1)
    rspn = s2.recv(64)
    if "Vf" in rspn:
        cve = "vulnerable"
        print "[+] "+ip+" vulnerable to CVE-2017-16241"
        with open("endbc-CVE_2017_16241.csv"):
            f.write(ip+","+cve)
    s2.close
if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='./endbc-check.py -r 10.0.0.1/24')
    parser.add_argument('-r', '--cidr', required=True, help='Target CIDR Range')
    args = parser.parse_args()
    cidr = args.cidr

    print "#############################################"
    print "#             Concierge Toolkit             #"
    print "#                                           #"
    print "#    AMAG EN Series CVE-2017-16241 Check    #"
    print "#############################################"
    print ""
    print "[*] Starting AMAG EN Series CVE_2017_16241 check."
    print ""
    if path.isfile("endbc-CVE_2017_16241.csv") == 0:
        with open("endbc-CVE_2017_16241.csv","a+")as f:
            f.write("rhost,cve-2017-16241\n")
    for ip in netaddr.IPNetwork(cidr).iter_hosts():
        try:
            amag_endbc_vulncheck()
        except (KeyboardInterrupt, SystemExit)as e:
            print "Keyboard Interrupt: Stopping all processes"
            sys.exit()
        except (socket.timeout, socket.error):
            pass
        except (IndexError):
            pass
    print ""
    print "[*] AMAG EN Series CVE-2017-16241 vuln check of "+cidr+" complete."
