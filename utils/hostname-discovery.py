#!/usr/bin/env python
# By Mike Kelly
# exfil.co
# @lixmk
#
# This script is part of the Concierge Toolkit
# https://github.com/lixmk/Concierge
#
import nmap
import re
import argparse
from os import path

keywords = {
    'generic':   ["physical","phys","pacs","pac","badge","access","door","controller","entry","exit","entrance"],
    'amag':      ["amag","en1dbc","en2dbc","m2150","symmetry","sms"],
    'hid':       ["hid","vertx","edge","evo","v1000","v2000","v2-v1000","v2-v2000","e400","eh400","es400","ehs400"],
    'mercury':   ["mercury","ep1501","ep1502","ep-1501","ep-1502"],
    'lenel':     ["lenel","lnl","2201","2202"],
    'honeywell': ["honeywell","pro3200","winpak","netaxs"],
    'axis':      ["axis","A1001"],
    'custom':    [],
}

global results
results = []

def scan():
    print "[*] Starting Scan"
    nm = nmap.PortScanner()
    if dns is not None:
        print "[*] Performing DNS lookups using DNS server: "+dns
        nm.scan(hosts=rhosts, arguments=('-sL -R --dns-server '+dns))
    else:
        print "[*] Performing DNS lookups using System DNS"
        nm.scan(hosts=rhosts, arguments='-sL -R')
    for host in nm.all_hosts():
        results.append(nm[host].hostname().lower()+","+host)
    print "[*] Scan Complete"

def parse():
    print "[*] Parsing Results"
    print ""
    print "  |------------------------|"
    print "  | # results |  category  |"
    print "  |-----------|------------|"
    for category in keywords.iterkeys():
        count = 0
        for keyword in keywords[category]:
            for host in results:
                if keyword in host.split(",")[0]:
                    with open("hostname-discovery-results.csv","a+")as f:
                        f.write(category+","+keyword+","+host+"\n")
                    count += 1
        print "  |"+str(count).rjust(10)+" | "+category.ljust(11)+"|"
    print "  |------------------------|"
    print ""
    print"[*] Parsing complete. Results written to ./hostname-discovery-results.csv"

def chkfile():
    if path.isfile("hostname-discovery-results.csv") == 0:
        with open("hostname-discovery-results.csv","a+")as f:
            f.write("category,keyword,hostname,ip address\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='./hostname-discovery.py -r 192.168.1.1/24')
    parser.add_argument('-r', '--rhosts', required=True, help='IP targets')
    parser.add_argument('-d', '--dns', help='Specify target DNS server (Default: System DNS)')
    parser.add_argument('-k', '--keywords', help='Additional custom keywords')
    args = parser.parse_args()
    rhosts = args.rhosts
    dns = args.dns
    newkeys = args.keywords
    if newkeys is not None:
        for word in newkeys.split(","):
            keywords['custom'].append(word.lower())
    print "################################################"
    print "#              Concierge Toolkit               #"
    print "#                                              #"
    print "# Hostname-based Phys Access Control Discovery #"
    print "################################################"
    print ""
    chkfile()
    scan()
    parse()
