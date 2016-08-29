# Concierge
A collection (eventually) of Physical Access Control and Monitoring attacks and utilities.
These will all eventually evolve into a more effective and user friendly set of tools, but
for now, simple bash scripts will do the job.

eh400.sh

  Usage: ./eh400.sh <action>
  Actions: exploit, cleanup
  All necessary variables will be entered during execution of the script.
  'exploit' leverages command injection vulnerability to:
  --Modify .htpasswd file to a known password value for "admin" user. This allows manual control via http(s).
  --Pushes "door" lock/unlock script to the EH400 (used by door.sh). This allows for control via cmdline.
  --Pulls IdentDB badge store and /etc/shadow from EH400.
  --Also checks /etc/shadow for known default password values.
  
  'cleanup' removes all copied or created files and restores the original htpasswd file.

vertx.sh

  Usage: ./vertx.sh <action>
  Actions: exploit, cleanup
  All necessary variables will be entered during execution of the script.
  'exploit' leverages command injection vulnerability to:
  --Creates new user, 'z', with password 'backdoor', and grants web access privs. This allows manual control via http(s).
  --Pushes "door" lock/unlock script to the VertX EVO (used by door.sh). This allows for control via cmdline.
  --Pulls IdentDB badge store and /etc/passwd from VertX EVO.
  --Also checks /etc/shadow for known default password values.

  'clean up' removes all copied or created files and deletes the 'z' user.

deploy.sh

  Usage: ./deploy.sh <ip> <mac>
  This script can be used for both EH400 and VertX EVO door controllers. This is a lighter weight script
  that only deploys the door script for use with door.sh.
 
door.sh

  Usage: ./door.sh <ip> <mac> <action>
  Actions: unlock, lock
  Example: ./door.sh 10.0.0.1 00:11:22:33:44:55 unlock
  Leverages the 'door' script deployed by either eh400.sh or vertx.sh.
  Use this script to trigger the locking mechanism from commandline
