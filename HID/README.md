# Concierge: HID  
Scripts related to the discovery and exploitation of HID global devices and services.  
  
##Acknowledgements
**Ricky "HeadlessZeke" Lawshae:** Ricky first identified and disclosed the vulnerability in the discoveryd service, which is exploited by these scripts. Additionally, Ricky's exploit code proved to be way more effective than my originals and have been implemented into Concierge. Check out the demo code from his DEF CON 24 talk at: <https://github.com/headlesszeke/defcon24-demos>
  
##References
Blog: <http://blog.trendmicro.com/let-get-door-remote-root-vulnerability-hid-door-controllers/>  
Disclosure: <http://www.zerodayinitiative.com/advisories/ZDI-16-223/>  
Blog: <http://exfil.co/2016/05/09/exploring-the-hid-eh400/>  
Blog: <http://exfil.co/2016/06/14/exploiting-vertx-door-controllers/>  
  
##Installation  
`git clone https://github.com/lixmk/Concierge`  
`pip install netaddr`  
  
##hidevo-exploit.py  
**Usage:** `./hidevo_exploit.py -r <rhost> -l <lhost> -c <cmd>`  
Commands Available:  
* unlock: Unlocks the associated door  
* lock:   Locks the associated door  
* blink:  Cycles a light pattern on the associated Badge Reader  
* steal:  Downloads and decodes the controllers IdentDB file, parsing out associated RFID card numbers. Hex values provided can be copy/pasted into proxmark for cloning. This has not yet been tested for iClass, but will be soon. Recovered badge values are saved to `./hidevo-badges.csv` along with targets IP address and hostname.  
  
##hidevo-discover.py  
**Usage:** `./hidevo_discover -r <target(s) in CIDR>`  
Uses HID's discoveryd service to identify HID EVO door controllers on the network. Identified door controllers are saved to `./hidevo-details.txt` which contains the full enumerated details of each identified HID EVO door controller. Currently only scans 1 ip at a time. Future version should allow for parallel scanning.  
  
##hidevo-discover.nse  
**Usage:** `nmap -sU -p 4070 --script=/path/to/NSE/hidevodiscover.nse <target(s)>`  
For use with nmap to scan larger network segments than the .py version can currently handle. MSF `db_import` has not been tested yet.  
