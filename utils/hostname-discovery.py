#!/usr/bin/env python
# This script is part of the Concierge Toolkit
# https://github.com/lixmk/Concierge
# 
# This script attempts to identify potentially interesting
# targets based on keywords in their hostnames. It can scan 
# both supplied network ranges or take in hosts from a supplied
# nmap xml file.

import argparse
import os
import sys
import logging
import csv
from collections import Counter
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser

logger = logging.getLogger()

def scan_ranges(ranges, dns=None):
    '''
    Performs a list scan on the provided ranges and returns an NmapReport object
    '''
    if dns is None: 
        dns = "-sL -R" 
    else:
        dns = "-sL -R --dns-server " + dns
    logger.info('DNS Value for scan_ranges: ' + str(dns))
    logger.info('Provided Ranges for scan_ranges: ' + str(ranges))
    print("Starting nmap scan against: " + ranges)
    nm = NmapProcess(ranges, options=dns)
    rc = nm.run()
    # use the nmap parser to return an object containing all the hosts
    parsed = NmapParser.parse(nm.stdout)
    logger.info('Returning {} hosts from scan_ranges'.format(len(parsed.hosts)))
    return parsed

def read_hosts_from_file(nmapxmlfile):
    '''
    Reads from a provided nmap XML file and returns an NmapReport object
    '''
    logger.info('Reading hosts from file: ' + str(nmapxmlfile))
    return NmapParser.parse_fromfile(nmapxmlfile)

def parse_hosts(nmapobject, custom_keywords=None):
    keywords = {
        'generic':   ["phys","pacs","pac","badge","access","door","controller","entry","exit","entrance"],
        'amag':      ["amag","en1dbc","en2dbc","m2150","symmetry","sms"],
        'hid':       ["hid","vertx","edge","evo","v1000","v2000","v2-v1000","v2-v2000","e400","eh400","es400","ehs400"],
        'mercury':   ["mercury","ep1501","ep1502","ep-1501","ep-1502"],
        'lenel':     ["lenel","lnl","2201","2202"],
        'honeywell': ["honeywell","pro3200","winpak","netaxs"],
        'axis':      ["axis","A1001"],
        'custom':    [],
    }
    # Add any custom keywords provided
    if custom_keywords is not None:
        keywords['custom'].extend(custom_keywords)
        logger.info("Added custom keywords: " + str(keywords['custom']))
    # Check the hostnames provided for the keywords
    matches = []
    for category in keywords:
        for keyword in keywords[category]:
            for host in nmapobject.hosts:
                for hostname in host.hostnames: #handles multiple hostnames per IP
                    if keyword in hostname:
                        matched_host = [category, keyword, hostname, host.ipv4]
                        report_writer(matched_host)
                        logger.info('Wrote {} to the outputfile'.format(matched_host))
                        matches.append(matched_host)
    return matches

def match_summary(matchlist):
    # Outputs a summary of matches
    print "################################################"
    print "#              Concierge Toolkit               #"
    print "#                                              #"
    print "# Hostname-based Phys Access Control Discovery #"
    print "################################################"
    print ""
    print "[*]  Results"
    if len(matchlist) == 0:
        print("No Matches on any categories")
    else:
        # Since we have some matches, output the summary header
        print "  |------------------------|"
        print "  | # Matches |  Category  |"
        print "  |-----------|------------|"
        # Now output a count for every category
        category_count = Counter(tuple([category[0] for category in matchlist]))
        for category in category_count.keys():
            count = category_count[category]
            print "  |"+str(count).rjust(10)+" | "+category.ljust(11)+"|"
        # Output the footer, after the counts
        print "  |------------------------|"
        print ""
        print"[*] Parsing complete. Results written to csv in current directory"

def report_writer(datalist, filename='hostname-discovery-results.csv'):
    logger.info('Running report_writer with data: ' + str(datalist))
    with open(filename, 'a+') as output_file:
        output_file.seek(0) # we need to count lines from the start of file
        csvwriter = csv.writer(output_file, delimiter=',')
        # if file is empty, add a csv header line at the top
        if len(output_file.readlines()) == 0:
            csvheaders = ["Category","Keyword","Hostname","IP Address"]
            csvwriter.writerow(csvheaders)
        #  then add data as rows
        csvwriter.writerow(datalist)

def main():
    """Main Execution"""
    parser = argparse.ArgumentParser(
        description='Scans provided ranges for interesting hostnames',
        epilog="Example: \n\t %s -r 10.0.0.0/16"%sys.argv[0])

    parser.add_argument(
        '-r','--rhosts',
        dest='rhosts',
        help='Range to scan (10.0.0.0/24)',
        )

    parser.add_argument(
        '-d','--dns',
        dest='dns',
        help='IP address for custom DNS. Default is system DNS',
        )

    parser.add_argument(
        '-f','--file',
        dest='file',
        help='Nmap XML file to parse instead of scanning',
        )

    parser.add_argument(
        '-k','--keywords',
        dest='keywords',
        help='Custom keywords to include. Comma delimited',
        )

    parser.add_argument(
        '-v', '--verbose',
        help="Verbose output",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
        )

    args = parser.parse_args() 


    #setup logging functions. Default is WARNING, but can set for INFO (--verbose)
    logger = logging.basicConfig(level=args.loglevel)

    if args.keywords: args.keywords = args.keywords.split(',')

    if args.rhosts:
        # Scan the provided rhosts and output the report
        hosts = scan_ranges(args.rhosts, args.dns)
        match_summary(parse_hosts(hosts, custom_keywords=args.keywords))
        # print("{} hosts returned".format(len(hosts.hosts)))
        exit()
    elif args.file:
        # Read the hosts fro mthe file and output the report
        hosts = read_hosts_from_file(args.file)
        # print("{} hosts returned".format(len(hosts.hosts)))
        match_summary(parse_hosts(hosts, custom_keywords=args.keywords))
        exit()
    else:
        print("You must supply either -r or -f")
        exit(1)
        #exit because they must supply either rhosts or an nmap file

if __name__ == '__main__':
    sys.exit(main())
