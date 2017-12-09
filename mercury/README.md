# Concierge: Mercury  
Various scripts (well, script) to discover and exploit Mercury Security OEM systems. Several vendors rebrand Mercury devices or use Mercury firmware on their own hardware.  
  
## ep-discover-snmp.py  
Makes an SNMP calls and parses responses to identify Mercury Security OEM door controllers. This script is known to identify EP-1501 and EP-1502 (and their many vanity names) door controllers but may also work for other Mercury OEM systems.  
   
**Usage:** `./ep-discover-snmp.py -r 10.0.0.1/24` 
  
**Note:** This script is slow. The preferred method of discovery is using the nmap NSE script in the utils/nse/ directory.
  
## ./nse/mercury-ep-snmp-discover.nse  
**Usage:** `nmap -sU -p 161 --script=mercury-ep-snmp-discover.nse <target(s)>`
Leverages SNMP to identify door controllers manufactured by, or using firmware from, Mercury Security. Mercury door controllers often rebranded by several other vendors including: Lenel, Honeywell, Premisys. Additionally, other manufactures use Mercury Security's firmware on their devices (such as KeriSystems' NXT series).
**Output:**
```
Nmap scan report 10.0.0.1
Host is up (0.12s latency).

PORT    STATE SERVICE
161/udp open  snmp
| mercury-ep-snmp-discover:
|   Description: EP-1502 Configuration Manager
|   Device Type: EP-1502
|   Firmware Verison: 1.19.4
|_  Build Number: 415
```  
