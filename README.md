# Concierge
A collection (eventually) of Physical Access Control and Monitoring attacks and utilities.
These will all eventually evolve into a more effective and user friendly set of tools, but
for now, simple bash scripts will do the job.

EH400-exploit.sh

	This scripts modified exploits the HID discoveryd vulnerability on a vulnerable 
	HID Edge EVo EH400 to replace the .htpasswd file with a password of your choosing. 
	The original .htpasswd files is backed up to allow for restoration to original 
	settings. (EH400-cleanup.sh)
	TODO: Acceptable as is. Will eventually be rolled into more complete toolkit.

EH400-exfil.sh

	This script should only be run after EH400-exploit.sh. This script will copy sensitive 
	files to the HID Edge EVO EH400 door controller's web root (/mnt/apps/web/) then uses 
	wget to pull them down. After files have been exfil'd, this scripts cleans the files.
	TODO: Build in checks to ensure files have been exfil'd correctly.

EH400-cleanup.sh

	Pretty straight forward. This script cleans after EH400-exploit.sh. It restores
	the backed-up .htpasswd file to it's proper location, effectively restoring the
	original 'admin' user password.
	TODO: Acceptable as is. Will eventually be depreciated
