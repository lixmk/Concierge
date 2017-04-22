# Concierge: Access Control Exploitation Kit  
Concierge is collection of various scripts and resources to aid in identification and exploitation of physical access control and monitoring systems.  
This kit is in very early stages and currently can only test for and exploit HID EVO (Edge and VertX) door controllers. That said, new tests exploits will be eventually released be added and I will continue to refine and update current scripts.  
  
## Most Recent Change:  
The Directory Structure: The directory structure has been modified to a vendor based layout. This has little effect now, but will in the future.  
  
The HID EVO discovery and exploitation scripts have been rewritten completely. The previous .sh scripts are completely obsolete and have been removed. Even the previous .py scripts in /pydev have been removed.  
  
This has been done because I realized there was a better way to execute commands that no longer (with one exception) require writing some form of agent or script to disk. The exploitation scripts now host the commands over port 8080 and tell the target HID EVO door controller to pipe the commands to /bin/sh via wget.  
  
Regarding that one exception. Well, that's a completely new attack. The HID EVO exploit script can now exfiltrate the IdentDB file (with `-c exfil`) and will automatically parse out badge numbers in a proxmark acceptable format, saving them all to .csv file.  
  
## Installation  
`git clone https://github.com/lixmk/Concierge`  
`pip install netaddr`  
  
## Usage  
Usage for each script can be found in the README.md file in each vendor's directory. At least until I get a wiki going.  
