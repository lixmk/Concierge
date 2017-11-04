# Concierge Toolkit: Utilities  
Miscellaneous scripts for stuff.  
  
## rfid-card-gen.py  
This script takes a facility code and card number and outputs proxmark3 hex values for HID 26 bit, HID Corp 35 bit (with facility code), and/or HID 37 bit badges.  
**Usage:** `./rfid-card-gen.py -b 26 -fc 111 -cn 2222`  
* The -b (--bitlen) switch is optional. If it is not set, the script will generate hex values for all bit lengths.  
* The script also ensures that facility codes and card numbers are with the acceptable ranges for each bit length.  
  
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

