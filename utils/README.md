# Concierge: Utilities  
Miscellaneous scripts for stuff  
  
## hid-cardgen.py  
This script takes a facility code and card number and outputs proxmark3 hex values for HID 26 bit, HID Corp 35 bit (with facility code), and/or HID 37 bit badges.  
**Usage:** `./hid-cardgen.py -b 26 -fc 111 -cn 2222`  
* The -b (--bitlen) switch is optional. If it is not set, the script will generate hex values for all bit lengths.  
* The script also ensures that facility codes and card numbers are with the acceptable ranges for each bit length.  
  
## hidevo-discover.nse  
**Usage:** `nmap -sU -p 4070 --script=/path/to/NSE/hidevodiscover.nse <target(s)>`  
For use with nmap to scan larger network segments than the .py version can currently handle. MSF `db_import` has not been tested yet.  
