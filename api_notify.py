#! /usr/bin/env python

import json
import argparse
import httplib
from urlparse import urlparse


def main():
    arg_parser = argparse.ArgumentParser(description='Submit API Call From Notification')
    arg_parser.add_argument(
        '-a',
        '--hostalias',
        help='Should be $HOSTALIAS$',
        required=True
    )
    arg_parser.add_argument(
        '-H',
        '--hostname',
        help='Should be $HOSTNAME$',
        required=True
    )
    arg_parser.add_argument(
        '-A',
        '--hostaddress',
        help='Should be $HOSTADDRESS$',
        required=True
    )
    arg_parser.add_argument(
        '-s',
        '--hoststate',
        help='Should be $HOSTSTATE$',
        required=True
    )
    arg_parser.add_argument(
        '-o',
        '--hostoutput',
        help='Should be $HOSTOUTPUT$',
        required=True
    )
    arg_parser.add_argument(
        '-t',
        '--shortdatetime',
        help='Should be $SHORTDATETIME$',
        required=True
    )
    arg_parser.add_argument(
        '-k',
        '--apikey',
        help='You API Key',
        required=True
    )
    arg_parser.add_argument(
        '-u',
        '--url',
        help='URL for API Server you are connecting to',
        required=True
    )
    arg_parser.add_argument(
        '-T',
        '--test',
        help='Dry run, no operations executed',
        action='store_true',
        default=False
    )
    arg_parser.add_argument(
        '-e',
        '--element',
        help='JSON element',
        action='append'
    )
    arg_parser.add_argument(
        '-d',
        '--delimiter',
        help='JSON element delimiter',
        default=':'

    )
    args = arg_parser.parse_args()

    host_alias = args.hostalias
    host_name = args.hostname
    host_address = args.hostaddress
    host_state = args.hoststate
    host_output = args.hostoutput
    current_date = args.shortdatetime
    api_key = args.apikey
    url_details = urlparse(args.url)
    url_server = url_details.netloc
    url_path = url_details.path

    headers = {
        'apikey': api_key,
        'content-type': "application/json"
    }

    build_json_data = {"Name": host_alias,
                       "HostName": host_name,
                       "HostAddress": host_address,
                       "State": host_state,
                       "Info": host_output,
                       "Timestamp": current_date} # Gather Required data for JSON

    if args.element:
        for element in args.element:
            if args.test is True:
                print "JSON element: {0}".format(element)
            key, value = element.split(args.delimiter)
            build_json_data[key] = value

    json_data = json.dumps(build_json_data) # Assemble JSON

    if args.test == True:
        print "Dry-Run Testing"
        print "----------"
        print 'Arguments'
        print "----------"
        print "HOSTALIAS Argument = {0}".format(args.hostalias)
        print "HOSTNAME Argument = {0}".format(args.hostname)
        print "HOSTADDRESS Argument = {0}".format(args.hostaddress)
        print "HOSTSTATE Argument = {0}".format(args.hoststate)
        print "HOSTOUTPUT Argument = {0}".format(args.hostoutput)
        print "SHORTDATETIME Argument = {0}".format(args.shortdatetime)

        print "----------"
        print 'Variables'
        print "----------"
        print "Server Variable = {0}".format(url_server)
        print "API Variable = {0}".format(api_key)
        print "JSON Variable = {0}".format(json_data)
        print "Headers Variable = {0}".format(headers)
        print "API Endpoint Variable = {0}".format(url_path)

    else:
        if url_details.scheme in ["https"]: # Determine if HTTPS or HTTP
            conn = httplib.HTTPSConnection(url_server) # Connecto to HTTPS Server
        else:
            conn = httplib.HTTPConnection(url_server) # Connect to HTTP Server
        conn.request("POST", url_details.path, json_data, headers) # Connect to endpoint
        res = conn.getresponse() # Get Response from HTTP Server
        data = res.read() # Read the Response from HTTP Server
        print(data.decode("utf-8")) # Display the response from HTTP Server
        conn.close() # Close Connection to HTTP Server


if __name__ == "__main__":
    main()
