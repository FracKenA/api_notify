#! /usr/bin/env python

import json
import argparse
import httplib
import base64
from urlparse import urlparse


def main():
    arg_parser = argparse.ArgumentParser(description='Submit API Call From Notification')
    arg_parser.add_argument(
        '-U',
        '--url',
        help='URL for API Server you are connecting to',
        required=True
    )
    arg_parser.add_argument(
        '-a',
        '--apikey',
        help='You API Key',
    )
    arg_parser.add_argument(
        '-p',
        '--password',
        help='API Password',
    )
    arg_parser.add_argument(
        '-u',
        '--username',
        help='API Username',
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
        help='JSON element delimiter : Semicolon is default',
        default=':'
    )
    arg_parser.add_argument(
        '-T',
        '--test',
        help='Dry run, no operations executed',
        action='store_true',
        default=False
    )
    args = arg_parser.parse_args()

    headers = {
            'content-type': "application/json"
        }

    build_json_data = {}  # Gather Required data for JSON
    
    url_details = urlparse(args.url)  # Convert URL into dic.

    if args.test:
        print "Dry-Run Testing"
        print "URL = {0}".format(args.url)
        print "Server Variable = {0}".format(url_details.netloc)
        print "API Endpoint Variable = {0}".format(url_details.path)

    # Test for API Key    
    if args.apikey:
        if args.test:
            print "API Key Variable = {0}".format(args.apikey)
        headers = {
            'apikey': args.apikey,
            'content-type': "application/json"
        }
        if args.test:
            print "API Key set, Using API Key"

    # Test for username and password, if present convert to base64. Default to API Key if API Key and Username and Password both present.
    if args.username:
        if args.test:
            print "Username = {0}".format(args.username)
        if args.password:
            if args.test:
                print "Password = {0}".format(args.password)
            auth64 = base64.encodestring('%s:%s' % (args.username, args.password)).replace('\n', '') # Convert Username and password to base64
            if args.test:
                print "Username Password Base64 = {0}".format(auth64)
            if args.apikey:
                if args.test:
                    print "Username Password Base 64 = {0}".format(upb64)
                    print "Multiple authentication methods provided, defaulting to API Key. Username and Password have been cleared"
                del auth64
            if auth64:
                headers = {
                    'Authorization': "Basic {0}".format(upb64),
                    'content-type': "application/json"
                }
                if args.test:
                    print "Username and Password set, Using Basic Auth"
    
    # Print Headers in Dryrun
    if args.test:
        print "Headers Variable = {0}".format(headers)

    # Add JSON elements to build_json_data dic above
    if args.element:
        for element in args.element:
            if args.test:
                print "JSON element: {0}".format(element)
            key, value = element.split(args.delimiter)
            build_json_data[key] = value

    json_data = json.dumps(build_json_data)  # Assemble JSON
    
    # Determine if HTTPS or HTTP
    if url_details.scheme in ["https"]:
        if args.test:
            print "Using HTTPS"
        conn = httplib.HTTPSConnection(url_details.netloc)  # Connecto to HTTPS Server
    else:
        if args.test:
            print "Using HTTP"
        conn = httplib.HTTPConnection(url_details.netloc)  # Connect to HTTP Server
    
    if not args.test:
        conn.request("POST", url_details.path, json_data, headers)  # Connect to endpoint
        res = conn.getresponse()  # Get Response from HTTP Server
        data = res.read()  # Read the Response from HTTP Server
        print(data.decode("utf-8"))  # Display the response from HTTP Server
        conn.close()  # Close Connection to HTTP Server
    else:
        print: "Dryrun test tomplete. Please review for any errors."


if __name__ == "__main__":
    main()
