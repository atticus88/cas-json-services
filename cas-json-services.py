#  The MIT License (MIT)
#
#  Copyright (c) 2014 Klint Holmes
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.

#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#!/usr/bin/python

import argparse
import getpass
import dataset
import json

parser = argparse.ArgumentParser(description='CAS Service to JSON')
parser.add_argument('-u', '--user', help='Username')
parser.add_argument('-H', help="Hostname")
parser.add_argument('-P',  help='Port')
parser.add_argument('-p',  help='Password', action='store_true')
parser.add_argument('-d', '--database', help='Database')
parser.add_argument('-o', help='Output file')
args = parser.parse_args()

if args.user and args.p and args.H and args.database:
	password = getpass.getpass("Password: ")
	db = dataset.connect('mysql://' + args.user + ':' + password + '@' + args.H + ':' + args.P + '/' + args.database)
	r = db.query("SELECT id, allowedToProxy, anonymousAccess, description, enabled, evaluation_order AS evaluationOrder, ignoreAttributes, name, serviceId, ssoEnabled, theme FROM RegisteredServiceImpl")
	
	services = []
	for s in r:
		services.append(s)
	
	config = { "services" : services }
	string =  json.dumps(config, indent=4)
	string = string.replace('"\u0001"', 'true')
	string = string.replace('"\u0000"', 'false')

	if args.o:
		f = open(args.o, 'w')
		f.write(string)
		f.close()
	else:
		print string
