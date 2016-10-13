# Concierge  
A collection (eventually) of Physical Access Control and Monitoring attacks and utilities. These will all eventually evolve into a more effective and user friendly set of tools, but for now, simple bash scripts will do the job.  

##Acknowledgements
**Ricky "HeadlessZeke" Lawshae:** Ricky first identified and disclosed the vulnerability in the discoveryd service, which is exploited by these scripts. Additionally, Ricky's exploit code proved to be way more effective than my originals and have been implemented into Concierge. Check out the demo code from his DEF CON 24 talk at: <https://github.com/headlesszeke/defcon24-demos>

##References
Blog: <http://blog.trendmicro.com/let-get-door-remote-root-vulnerability-hid-door-controllers/>  
Disclosure: <http://www.zerodayinitiative.com/advisories/ZDI-16-223/>  
Blog: <http://exfil.co/2016/05/09/exploring-the-hid-eh400/>  
Blog: <http://exfil.co/2016/06/14/exploiting-vertx-door-controllers/>

## Pydev
These scripts are the "future" versions of the .sh scripts. Once all the .sh scripts have been ported to python and tested, they .sh scripts will be depreciated (but probably saved in ./old or something, just in case).  
## Notes
The "mass" .py scripts require netaddr which can be installed with `pip install netaddr`  
