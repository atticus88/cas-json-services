#    CAS Databse Services to JSON
#    Copyright (C) 2014  Klint Holmes
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
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
