# Concierge Toolkit: HID  
Scripts related to the discovery and exploitation of HID Global devices and services.  
  
## Acknowledgements
**Ricky "HeadlessZeke" Lawshae:** Ricky first identified and disclosed the vulnerability in the discoveryd service, which is exploited by these scripts. Additionally, Ricky's exploit code proved to be way more effective than my originals and have been implemented into Concierge. Check out the demo code from his DEF CON 24 talk at: <https://github.com/headlesszeke/defcon24-demos>
  
## References
Blog: <http://blog.trendmicro.com/let-get-door-remote-root-vulnerability-hid-door-controllers/>  
Disclosure: <http://www.zerodayinitiative.com/advisories/ZDI-16-223/>  
Blog: <http://exfil.co/2016/05/09/exploring-the-hid-eh400/>  
Blog: <http://exfil.co/2016/06/14/exploiting-vertx-door-controllers/>  
  
## evo-exploit.py  
This script exploits a root privileged command injection vulnerability (ZDI-16-223) to perform the actions listed below.  
**Usage:** `./evo-exploit.py -r 10.0.0.1 -l 192.168.1.1 -c <cmd>`  
Commands Available:  
* unlock:  Unlocks the associated door(s)  
* lock:    Locks the associated door(s)  
* blink:   Cycles a light pattern on the associated Badge Reader(s)  
* exfil:   Downloads and decodes the controllers IdentDB file, parsing out associated RFID card numbers. Hex values provided can be copy/pasted into proxmark for cloning. This has not yet been tested for iClass, but will be soon. Recovered badge values are saved to `./hid-evo-badges.csv` along with targets IP address and hostname.  
* implant: Implants a backdoor badge value into the door controller. PM3 Hex: `2004060a73`. iClass Blk7 (Encrypted): `8b0c4cf554bca3fe` 
  
## evo-discover.py  
Uses HID's discoveryd service to identify HID EVO door controllers on the network. Identified door controllers are saved to `./hid-evo-details.csv` which contains the full enumerated details of each identified HID EVO door controller. This script is slow, the preferred method is the nmap .nse in the utils/nse directory.  
**Usage:** `./evo-discover -r 10.0.0.1/24` 
  
**Note:** This script is slow. The preferred method of discovery is using the nmap NSE script in the utils/nse/ directory.  
  
## ./nse/hid-evo-discover.nse  
**Usage:** `nmap -sU -p 4070 --script=hid-evo-discover.nse <target(s)>`
Recreates HID's discoveryd structure to identify door HID Edge EVO and VertX EVO door controllers.
**Output:**
```
Nmap scan report 10.0.0.1
Host is up (0.12s latency).

PORT     STATE         SERVICE
4070/udp open|filtered unknown
| hid-discoveryd-enum:
|   MAC Address: 00:06:8E:FF:FF:FF
|   Host Name: EdgeEH400-001
|   Internal IP: 10.0.0.1
|   Device Type: EH400
|   Firmware Version: 3.5.1.1483
|_  Build Date: 07/02/2015
MAC Address: 00:06:8E:XX:XX:XX (HID)
```  
