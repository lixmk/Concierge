#!/usr/bin/env python
# By Mike Kelly
# exfil.co
# @lixmk
#
# This script is part of the Concierge Toolkit
# https://github.com/lixmk/Concierge
#
# Takes Facility Code and Card number to generate proxmark3 hex values for card cloning
# Currently capable of generating 26 bit HID, 35 bit HID Corp, and 37 bit HID (with facility code) formats 
#

import argparse

def bl26(fc, cn):
    global pmhex
    # 44 bit header
    header = "000000100000000001"
    # checking input sanity
    if int(fc) > 255:
        print "[!] Facility code too high for 26 bit HID card."
    elif int(cn) > 65535:
        print "[!] Card number too high for 26 bit HID card."
    else:
        # generating output
        bfc = bin(int(fc))[2:].zfill(8)
        bcn = bin(int(cn))[2:].zfill(16)
        bits = bfc+bcn
        # even parity calc
        epf = bits[:12]
        if int(str(epf).count('1')) % 2 == 0:
            epb = "0"
        else:
            epb = "1"
        # odd parity calc
        opf = bits[12:]
        if int(str(opf).count('1')) % 2 == 0:
            opb = "1"
        else:
            opb = "0"
        # outputing
        bcard = header+epb+bfc+bcn+opb
        pmhex = hex(int(bcard, 2))[2:].zfill(10)
        print "26 bit card hex: "+pmhex

def bl35(fc, cn):
    global pmhex
    # 44 bit header
    header = "000000101"
    # checking input sanity
    if int(fc) > 4095:
        print "[!] Facility code too high for 35 bit HID card."
    elif int(cn) > 1048575:
        print "[!] Card number too high for 35 bit HID card."
    else:
        # generating output
        bfc = bin(int(fc))[2:].zfill(12)
        bcn = bin(int(cn))[2:].zfill(20) 
        bits = list(bfc+bcn)
        # first parity calc (even)
        pf1 = bits[0]+bits[1]+bits[3]+bits[4]+bits[6]+bits[7]+bits[9]+bits[10]+bits[12]+bits[13]+bits[15]+bits[16]+bits[18]+bits[19]+bits[21]+bits[22]+bits[24]+bits[25]+bits[27]+bits[28]+bits[30]+bits[31]
        if int(str(pf1).count('1')) % 2 == 0:
            pb1 = "0"
        else:
            pb1 = "1"
        bits = list(pb1+bfc+bcn)
        # second parity calc (odd)
        pf2 = bits[0]+bits[1]+bits[3]+bits[4]+bits[6]+bits[7]+bits[9]+bits[10]+bits[12]+bits[13]+bits[15]+bits[16]+bits[18]+bits[19]+bits[21]+bits[22]+bits[24]+bits[25]+bits[27]+bits[28]+bits[30]+bits[31]
        if int(str(pf2).count('1')) % 2 == 0:
            pb2 = "1"
        else:
            pb2 = "0"
        bits = pb1+bfc+bcn+pb2
        # third parity calc (odd)
        if int(str(bits).count('1')) % 2 == 0:
            pb3 = "1"
        else:
            pb3 = "0"
        # outputing
        bcard = header+pb3+pb1+bfc+bcn+pb2
        pmhex = hex(int(bcard, 2))[2:].zfill(10)
        print "35 bit card hex: "+pmhex

def bl37(fc, cn):
    global pmhex
    # checking input sanity
    if int(fc) > 65535:
        print "[!] Facility code too high for 37 bit HID card."
    elif int(cn) > 524287:
        print "[!] Card number too high for 37 bit HID card."
    else:
        bfc = bin(int(fc))[2:].zfill(16)
        bcn = bin(int(cn))[2:].zfill(19)
        cardbits = bfc+bcn
        # even parity calc
        epf = cardbits[:18]
        if int(str(epf).count('1')) % 2 == 0:
            epb = "0"
        else:
            epb = "1"
        # odd parity calc
        opf = cardbits[17:]
        if int(str(opf).count('1')) % 2 == 0:
            opb = "1"
        else:
            opb = "0"
        # outputing
        bcard = epb+bfc+bcn+opb
        pmhex = hex(int(bcard, 2))[2:].zfill(10)
        print "37 bit card hex: "+pmhex

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='./hid-cardgen.py -b 26 -fc 111 -cn 2222')
    parser.add_argument('-b', '--bitlen', help='Target output bit length of card. (26, 35, or 37)')
    parser.add_argument('-fc', '--fc', required=True, help='Facility code of card')
    parser.add_argument('-cn', '--cn', required=True, help='Card number of card')
    args = parser.parse_args()
    bitlen = args.bitlen
    fc = args.fc
    cn = args.cn
    # only 26 bit
    if bitlen == "26":
        print "Generating 26 bit card hex for FC: "+fc+" and CN: "+cn
        print ""
        bl26(fc, cn)

    # only 35 bit
    elif bitlen == "35":
        print "Generating 35 bit card hex for FC: "+fc+" and CN: "+cn
        print ""
        bl35(fc, cn)

    # only 37 bit
    elif bitlen == "37":
        print "Generating 37 bit card hex for FC: "+fc+" and CN: "+cn
        print ""
        bl37(fc, cn)

    # all
    else:
        print "Generating hex values for FC: "+fc+" and CN: "+cn
        print ""
        bl26(fc, cn)
        bl35(fc, cn)
        bl37(fc, cn)
