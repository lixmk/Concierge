#!/usr/bin/env python
# By Mike Kelly
# exfil.co
# @lixmk
#
# This script is part of the Concierge Toolkit
# https://github.com/lixmk/Concierge
#
# Uses AMAG Technologies discovery protocol to identify EN- Series door controllers in a cidr range.
# Also tests identified controllers for CVE-2017-16241 vulnerability. This check has not been thoroughly tested for false positive/negatives
# Identified controllers are saved to endbc-details.csv
#

import socket
import argparse
import netaddr
import re
import sys
from time import sleep
from os import path
from os import geteuid

# Discover AMAG EN-DBC Door Controllers
def amag_endbc_discover_udp():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 49107))
    s.setblocking(0)
    pkt0 = '000004b2ab9913de000001a000000000bddf3c00000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'.decode('hex')
    s.sendto(pkt0, (str(ip), 49107))
    s.settimeout(.5)
    rsp = s.recv(1024)
    rspn = re.findall("[^\x00-\x1F\x7F-\xFF]{4,}", re.sub('(    )', '', rsp))
    s.close
    if len(rspn) > 0:
        if "1DBC" in rspn[2]:
            print "[+] AMAG EN-"+rspn[2][:4]+" response received from: "+str(ip)
            print "    Device Type: EN-"+rspn[2][:4]
            print "    Hostname: "+rspn[3]
            print "    Version: "+rspn[1]
            if vulncheck == 1:
                s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                pkt1 = '0230315a5a235666304439'.decode('hex')
                s2.setblocking(0)
                s2.settimeout(.5)
                s2.connect((str(ip), 3001))
                s2.send(pkt1)
                if "Vf" in s2.recv(64):
                    cve = "vulnerable"
                    print "    CVE-2017-16241: Vulnerable"
                else:
                    cve = "not vulnerable"
                    print "    CVE-2017-16241: Not vulnerable"
                s2.close
            else:
                cve = "not checked"
            with open("endbc-details.csv","a+")as f:
                f.write(str(ip)+",EN-"+rspn[2][:4]+","+rspn[3]+","+rspn[1]+","+cve+"\n")
        if "2DBC" in rspn[2]: 
            print "[+] AMAG EN-"+rspn[2][:4]+" response received from: "+str(ip)
            print "    Device Type: EN-"+rspn[2][:4]
            print "    Hostname: "+rspn[3]
            print "    Version: "+re.sub('[()]', '',rspn[13])
            if vulncheck == 1:
                s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                pkt1 = '0230315a5a235666304439'.decode('hex')
                s2.setblocking(0)
                s2.settimeout(0.5)
                s2.connect((str(ip), 3001))
                s2.send(pkt1)
                if "Vf" in s2.recv(64):
                    cve = "vulnerable"
                    print "    CVE-2017-16241: Vulnerable"
                else:
                    cve = "not vulnerable"
                    print "    CVE-2017-16241: Not vulnerable"
                s2.close
            else:
                cve = "not checked"
            with open("endbc-details.csv","a+")as f:
                f.write(str(ip)+",EN-"+rspn[2][:4]+","+rspn[3]+","+re.sub('[()]', '',rspn[13])+","+cve+"\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='./endbc-discover.py -r 10.0.0.1/24 -v')
    parser.add_argument('-r', '--rhosts', required=True, help='Target CIDR Range')
    parser.add_argument('-v', '--vulncheck', action='store_true', help='Optional. Perform CVE-2017-16241 vulnerability check')
    args = parser.parse_args()
    rhosts = args.rhosts
    vulncheck = args.vulncheck
    print "#############################################"
    print "#             Concierge Toolkit             #"
    print "#                                           #"
    print "# AMAG EN- Series Door Controller Discovery #"
    print "#############################################"
    print ""
    try:
        if not geteuid() == 0:
            print "[!] This script must be run with root privileges."
            sys.exit()
        print "[!] This script is slow and has known problems with occasional false negatives for EN-1DBC controllers."
        print "[!] The preferred method of discovery for AMAG EN series controllers is via the nmap nse script `utils/nse/`"
        print ""
        sleep(5)
        print "[*] Starting door controller discovery."
        if path.isfile("endbc-details.csv") == 0:
            with open("endbc-details.csv","a+")as f:
                f.write("rhost,device type,hostname,firmware version,cve-2017-16241\n")
        for ip in netaddr.IPNetwork(rhosts).iter_hosts():
            amag_endbc_discover_udp()
    except (KeyboardInterrupt, SystemExit)as e:
        print ""
        print "Keyboard Interrupt: Stopping all processes"
        sys.exit()
    except (socket.timeout, socket.error):
        pass
    except (IndexError):
        pass
    print "[*] AMAG EN series discovery of "+rhosts+" complete."
