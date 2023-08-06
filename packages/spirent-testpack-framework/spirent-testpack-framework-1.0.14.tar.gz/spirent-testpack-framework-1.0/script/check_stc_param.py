#!/usr/bin/env python
"""
This file is used to get the STC port parameters(phy, speed, ...). Need run in the testpack Python 3 venv.
Example:python script/check_stc_param.py -l 10.109.113.33 -c plathw-amara-03.calenglab.spirentcom.com -s 3 -p 5
"""
import os
import sys
import argparse
from stcrestclient import stchttp

DEFAULT_HTTP_TIMEOUT_SEC = 120
USER_NAME = 'spirent'
SESSION_NAME = 'testpack-' + os.path.basename(__file__)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '-l', '--lab_server', help='lab server ip')
arg_parser.add_argument(
    '-c', '--chassis', help='chassis ip')
arg_parser.add_argument(
    '-s', '--slot', help='slot number')
arg_parser.add_argument(
    '-p', '--port', help='port number')

args = arg_parser.parse_args()
if args.lab_server is None:
    sys.exit("Lab server ip must be specified")
if args.chassis is None:
    sys.exit("Chassis ip must be specified")
if args.slot is None:
    sys.exit("Slot number must be specified")
if args.port is None:
    sys.exit("Port number  must be specified")

# Connect to lab server
print("<--------Connecting Lab Server...----------->")
stc = stchttp.StcHttp(args.lab_server, timeout=DEFAULT_HTTP_TIMEOUT_SEC)

#Create sessoin
session = stc.new_session(USER_NAME, SESSION_NAME)

#Create objects
print("<--------Connecting Chassis...-------------->")
project = stc.create('project')
port = stc.create('port', under=project)
csp = "//%s/%s/%s" % (args.chassis, args.slot, args.port)
stc.config(port, location=csp)

print("<--------Attaching port...------------------>")
stc.perform('attachPorts', autoConnect='true', portList=[port])

print("<--------Getting parameters...-------------->")
supported_phy = stc.get(port, 'SupportedPhys')
supported_phy_list = supported_phy.split(' ')
supported_phy_list = [''.join(phy.lower().split('_')) for phy in supported_phy_list]
active_phy = stc.get(port, 'ActivePhy')
supported_speed = stc.get(active_phy, 'SupportedSpeeds')


print("<--------Disconnecting...------------------->")
stc.disconnectall()
stc.end_session()

print("The parameters for %s are:" % csp)
print("Supported phy: %s" % supported_phy_list[0])
print("Supported speed: %s" % supported_speed)
