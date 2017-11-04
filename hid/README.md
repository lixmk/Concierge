# Concierge: HID  
Scripts related to the discovery and exploitation of HID global devices and services.  
  
## Acknowledgements
**Ricky "HeadlessZeke" Lawshae:** Ricky first identified and disclosed the vulnerability in the discoveryd service, which is exploited by these scripts. Additionally, Ricky's exploit code proved to be way more effective than my originals and have been implemented into Concierge. Check out the demo code from his DEF CON 24 talk at: <https://github.com/headlesszeke/defcon24-demos>
  
## References
Blog: <http://blog.trendmicro.com/let-get-door-remote-root-vulnerability-hid-door-controllers/>  
Disclosure: <http://www.zerodayinitiative.com/advisories/ZDI-16-223/>  
Blog: <http://exfil.co/2016/05/09/exploring-the-hid-eh400/>  
Blog: <http://exfil.co/2016/06/14/exploiting-vertx-door-controllers/>  
  
## Installation  
`git clone https://github.com/lixmk/Concierge`  
`pip install netaddr`  
  
## hid-evo-exploit-ZDI\_16\_223.py  
This script exploits a root privileged command injection vulnerability (ZDI-16-223) to perform the actions listed below.  
**Usage:** `./hid-evo-exploit-ZDI_16_223.py -r <rhost> -l <lhost> -c <cmd>`  
Commands Available:  
* unlock:  Unlocks the associated door(s)  
* lock:    Locks the associated door(s)  
* blink:   Cycles a light pattern on the associated Badge Reader(s)  
* exfil:   Downloads and decodes the controllers IdentDB file, parsing out associated RFID card numbers. Hex values provided can be copy/pasted into proxmark for cloning. This has not yet been tested for iClass, but will be soon. Recovered badge values are saved to `./hid-evo-badges.csv` along with targets IP address and hostname.  
* implant: Implants a backdoor badge value into the door controller. PM3 Hex: `2004060a73`. iClass Blk7 (Encrypted): `8b0c4cf554bca3fe` 
  
## hid-evo-discover.py  
**Usage:** `./hid-evo-discover -r <target(s) in CIDR>`  
Uses HID's discoveryd service to identify HID EVO door controllers on the network. Identified door controllers are saved to `./hid-evo-details.csv` which contains the full enumerated details of each identified HID EVO door controller. Currently only scans 1 ip at a time. Future version should allow for parallel scanning.  
