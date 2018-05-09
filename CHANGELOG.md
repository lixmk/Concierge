## Pseudo Changelog:  
**05/09/18**  
Merged pull request from @atucom that completely rebuilt the hostname-discovery.py script. The script now has the option to parse nmap xml files instead of actively making DNS requests first.  

**05/03/18**  
Adds new discovery script for Lantronix Modules, often found door controllers and other access control related devices.  

**12/09/17: HushCon Seattle Edition.**  
This update contains a bunch of new scripts including exploits for AMAG's EN series of door controllers (CVE-2017-17241). Concierge is now, officially, a multi-vendor tool. More specifically:  
* Discovery and exploit scripts for AMAG EN Series door controllers (EN-1DBC, EN-1DBC+, and EN-2DBC). Works on all versions under default conditions. (./amag/)  
* Nmap NSE script for AMAG EN Series controller identification.  
* Discovery script for Mercury based Door controllers via SNMP. Both in slow python and faster nmap .nse (Mercury Security, Lenel, some Honeywell, and more).  
* A hostname based discovery script that leverages performs host name looks up and checks for generic and vendor specific keywords in hostnames.  
* Various minor updates and/or bug fixes to most scripts.  
* More renaming because I can't decide on a final convention.  
  
**11/4/17**  
  
* Created this CHANGELOG file and removed changelog info from primary README file  
* Merged PR for HID V1000 specific conditions in hid-evo-exploit.py (now renamed evo-exploit.py)  
* Renamed most scripts for some kind of uniformity. Most are now `./<vendor>/<model>-<action>.<ext>`.  
* Other various uniformity updates, primarily to printed banners  
* Changed LICENSE to MIT for simplicity  
  
**10/13/17**

* hidevo-exploit.py now modifies it's payloads based on the device type reported by the device. This makes exploitation more reliable. Not all device types currently have working code for every command. Unknown device types create a notification and and then hidevo-exploit.py defaults to the most common version of that payload. If you run into an unknown device type, let me know and we can work to get commands functioning.
* Moved hidevo-discover.nse to `./utils`
* Created hid-cardgen.py script in `./utils`. This script takes a facility code and card number as input and outputs proxmark3 hex values for HID 26 bit, HID Corp 35 bit, and HID 37 bit (with facility code). Useful for cloning cards from FC and Card number only.


**4/23/17**
Added implant feature to hidevo-exploit.py. Implants a known badge value into the HID EVO Door Controller's DB files.

**4/22/17**
The Directory Structure: The directory structure has been modified to a vendor based layout. This has little effect now, but will in the future.

The HID EVO discovery and exploitation scripts have been rewritten completely. The previous .sh scripts are completely obsolete and have been removed. Even the previous .py scripts in /pydev have been removed.

This has been done because I realized there was a better way to execute commands that no longer (with one exception) require writing some form of agent or script to disk. The exploitation scripts now host the commands over port 8080 and tell the target HID EVO door controller to pipe the commands to /bin/sh via wget.

Regarding that one exception. Well, that's a completely new attack. The HID EVO exploit script can now exfiltrate the IdentDB file (with `-c exfil`) and will automatically parse out badge numbers in a proxmark acceptable format, saving them all to .csv file.
