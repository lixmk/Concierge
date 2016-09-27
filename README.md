# Concierge  
A collection (eventually) of Physical Access Control and Monitoring attacks and utilities. These will all eventually evolve into a more effective and user friendly set of tools, but for now, simple bash scripts will do the job.  

##Acknowledgements
**Ricky "HeadlessZeke" Lawshae:** Ricky first identified and disclosed the vulnerability in the discoveryd service, which is exploited by these scripts. Additionally, Ricky's exploit code proved to be way more effective than my originals and have been implemented into Concierge. Check out the demo code from his DEF CON 24 talk at: <https://github.com/headlesszeke/defcon24-demos>

##References
Blog: <http://blog.trendmicro.com/let-get-door-remote-root-vulnerability-hid-door-controllers/>  
Disclosure: <http://www.zerodayinitiative.com/advisories/ZDI-16-223/>  
Blog: <http://exfil.co/2016/05/09/exploring-the-hid-eh400/>  
Blog: <http://exfil.co/2016/06/14/exploiting-vertx-door-controllers/>

##eh400.sh  
**Usage:** `./eh400.sh <action>`  
Actions: exploit, cleanup  
All necessary variables will be entered during execution of the script.  

**exploit:** Leverages command injection vulnerability to:  
* Modify .htpasswd file to a known password value for "admin" user. This allows manual control via http(s).  
* Pushes remote agent script to the EH400 (used by triggeragent.sh). This allows for control via cmdline.  
* Pulls IdentDB badge store and /etc/shadow from EH400.  
* Also checks /etc/shadow for known default password values.  
    
**cleanup:** Removes all copied or created files and restores the original htpasswd file.  
  
##vertx.sh  
**Usage:** `./vertx.sh <action>`  
Actions: exploit, cleanup  
All necessary variables will be entered during execution of the script.  
**exploit:** Leverages command injection vulnerability to:  
* Creates new user, 'z', with password 'backdoor', and grants web access privs. This allows manual control via http(s).  
* Pushes remote agent script to the VertX EVO (used by triggeragent.sh). This allows for control via cmdline.  
* Pulls IdentDB badge store and /etc/passwd from VertX EVO.  
* Also checks /etc/passwd for known default password values.  

**clean up:** Removes all copied or created files and deletes the 'z' user.  
  
##agentdeploy.sh  
**Usage:** `./agentdeploy.sh <ip> <mac>`  
This script can be used for both EH400 and VertX EVO door controllers. This is a lighter weight script that only deploys the agent script for use with triggeragent.sh.  
  
##triggeragent.sh  
**Usage:** `./triggeragent.sh <ip> <mac> <action>`  
Actions: unlock, lock, blink  
Example: `./triggeragent.sh 10.1.1.10 00:11:22:33:44:55 unlock`  
Leverages a previously deployed agent script deployed to lock/unlock a door controller's associated locking mechanism or blink the LEDs on the associated reader. Further testing against V1000 required.  

'blink' flashes the LED lights on an associated RFID reader. Used to help locate the exploited door. This has only been tested on HID iClass (and similar) readers, but should work on any reader with external LEDs.  
  
##agentclean.sh  
**Usage:** `./agentclean.sh <ip> <mac>`  
Removes agent script from targeted door controller. Used to clean up after agentdeploy.sh and triggeragent.sh. If you've used eh400.sh or vertx.sh to exploit the targets, use them again with the cleanup action.  
  
##massdeploy.sh  
**Usage:** `./massdeploy.sh <attacker ip> <target(s)>`
Example: `./massdeploy.sh 10.0.0.1 10.1.1.0/24`  
All targets must be provided in nmap acceptable format. Currently, input files are not accepted. This script simply automates findings door controllers and deploying agents.  
  
##massclean.sh  
**Usage:** `./massclean.sh <target(s)>`  
Example: `./massclean.sh 10.10.0.1/24`  
  
##hid-discoveryd-enum.nse  
**Usage:** `nmap -sU -p 4070 --script hid-discoveryd-enum <target(s)>`  
Simple nmap script to leverage the fuctionality of the discoveryd service to identify HID EVO door controllers and enumerate system information.
This nse is located in the tools directory. Simply copy it to nmap's script directory.
  
##Notes
Testing of these scripts were completed against three seperate HID Door controllers:  
* Edge EVO EH400  
* VertX EVO V2000  
* VertX EVO V1000  
  
A wiki will be on the way shortly enough to provide more thorough information.  
  
##TO DO
* Combine eh400.sh and vertx.sh into single script. Evaluate better ways to handle variables. Maybe just provide target IP and use discover to pull MAC.  
* Further develop capabilities of agent Modify controller agent to limit command injections.
