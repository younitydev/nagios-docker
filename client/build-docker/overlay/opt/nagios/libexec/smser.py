#!/usr/bin/env python
import httplib
import base64
import optparse
import sys
from urllib import quote


AuthToken = base64.b64encode('put-your-token-here')
From = '%2B' + '972524735987'
To = '%2B' + '972544765150'
sms_newline_encodig = "%0a"
Text = None

parser = optparse.OptionParser()
parser.add_option("--to", '-t', dest="to", action='store', default=None, help="Phone number of the receiver")
parser.add_option("--data", '-d', dest="data", action='store', default=None, help="Text to send in the SMS body")
(options, args) = parser.parse_args(sys.argv[1:])

if (options.to == None) or (options.data == None):
	parser.print_help()
	sys.exit()

Text = quote(options.data)
To = '%2B' + options.to

Text = Text.replace("_NEWLINE_","%0a")

body = "Body=%s&From=%s&To=%s" % (Text, From, To)
headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic %s" % AuthToken}
try:
	h1 = httplib.HTTPSConnection('api.twilio.com:443')
	h1.request("POST", "/2010-04-01/Accounts/AC5a62756ca190814da7e2c8bd3926d253/SMS/Messages", body, headers)
	response = h1.getresponse()
	response_body = response.read()
	print response_body
except:
	print "Unexpected error:", sys.exc_info()[0]
	raise