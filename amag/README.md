# Concierge: AMAG  
Various scripts to discovery and exploit AMAG Symmetry SMS and AMAG EN-1DBC, EN-1DBC+, and EN-2DBC door controllers.  
  
## References  
* <https://www.secureworks.com/research/advisory-2017-001>  
* <https://cve.mitre.org/cgi-bin/cvename.cgi?name=cve-2017-16241>  
* <http://exfil.co/2017/12/10/cve-2017-16241/>  
  
## endbc-exploit.py  
This script exploits CVE-2017-16241 to trigger commands on the vulnerable door controller. This effectively allows for the full control of the device. Affected devices include: AMAG's EN-1DBC, EN-1DBC+, and EN-2DBC door controllers. This vulnerability can be used to trigger locking mechanisms over the network. Additionally, it allows for injection of known card values into the controllers internal DB. Use of these "backdoor badges" does not create an alarm event in the AMAG Symmetry SMS software under default configurations.  
  
**Usage:** `./endbc-exploit.py -c <cmd> -r 10.0.0.1`  
Actions: unlock, lock, disable, enable, implant, remove  
  
**unlock:** Unlocks the locking mechanism.  
**lock:** Locks the locket mechanism.  
**disable:** Disables the attached reader. Could be used to prevent or delay physical access.  
**enable:** Enables the attached reader.  
**implant:** Add new badge values to the door controller database. Requires `-fc <facility code` and `-cn <card number>`. Optional `-pn <pin number>` defaults to 1234.  
**remove:** Delete badge values from the door controller database. Requires `-fc <facility code` and `-cn <card number>`.  
  
## endbc-discover.py  
This script uses a recreation of AMAG's purpose built discovery protocol to identify door controllers across a provided cidr range. Delivers basic information like hostname, device type, firmware version. Also contains a -v switch to check if the discovered door controller is vulnerable to CVE-2017-16241.  
  
**Usage:** `./endbc-discover.py -r 10.0.0.1/24 -v`  

**Note:** This script is slow and has problems with known false negatives on EN-1DBC. The preferred method of discovery is using the nmap NSE script in the utils directory.  
  
## endbc-check.py  
This script attempts to exploit the CVE-2017-16241 across a provided cidr range with a simple version check command to confirm vulnerability. Can be used as a secondary discovery method if the UDP discovery method doesn't work.  
  
**Usage:** `./endbc-check.py -r 10.0.0.1/24`  
  
## symmetry-pcap2cards.py  
This script pulls card number and facility code out of pcaps that contain traffic between an AMAG Symmetry SMS and AMAG networked door controllers.  
**Usage:** `./symmetry-pcap2cards.py -f <pcap file>`  
  
## ./nse/amag-endbc-discover.nse  
**Usage:** `nmap -sU -p 49107 --disable-arp-ping --script=amag-endbc-discover.nse <target(s)>`
Recreates AMAG's proprietary discovery service to identify EN-1DBC, EN-1DBC+, and EN-2DBC. Testing shows that the --disable-arp-ping flag helps eliminate false-negatives when scanning your own subnet.
**Output:**
```
Nmap scan report 10.0.0.1
Host is up (0.12s latency).

PORT      STATE         SERVICE
49107/udp open|filtered unknown
| amag-endbc-discover:
|   Device Type: AMAG EN-1DBC
|_  Firmware Version: 03.60
MAC Address: 00:15:BD:XX:XX:XX (Group 4 Technology)
```  
