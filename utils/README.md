# Concierge: Utilities  
Miscellaneous scripts for stuff  
  
## rfid-card-gen.py  
This script takes a facility code and card number and outputs proxmark3 hex values for HID 26 bit, HID Corp 35 bit (with facility code), and/or HID 37 bit badges.  
**Usage:** `./hid-cardgen.py -b 26 -fc 111 -cn 2222`  
* The -b (--bitlen) switch is optional. If it is not set, the script will generate hex values for all bit lengths.  
* The script also ensures that facility codes and card numbers are with the acceptable ranges for each bit length.  
  
## hostname-discovery.py  
This script uses DNS lookups and compares hostnames against keyword to help identify systems and devices potentially associated with physical access controls. Likely to contain lots of false positives, but it's a place to start. Initial testing shows that it takes rougly 4-6 minutes for a /16. See `keywords = []` section for current keywords. Requires python-nmap: `pip install python-nmap`  
**Usage:** `./hostname-discovery.py -r 10.0.0.0/16 -k phys,badge,access -d ns01.target.tld`  
* -r, --rhosts, required. Target ip(s) in nmap format  
* -d, --dns, optional. DNS server to use. Default uses system's DNS.  
* -k, --keywords, optional. Additonal keywords to search for beyond default. Comma separated, no whitespace.  
  
## lantronix-discover.py  
This script uses Lantronix's proprietary discovery protocol to identify devices with Lantronix modules. Lots of different devices use Lantronix modules, including door controllers. More work needs to be done to parse the response, currently only parses out MAC address.  
**Useage:** `./lantronix-discover.py -r 10.0.0.0/24`  
* -r, --rhosts, required. Target ip(s) in cidr.  
