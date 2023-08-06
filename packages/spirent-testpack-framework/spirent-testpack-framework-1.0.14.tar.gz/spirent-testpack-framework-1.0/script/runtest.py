#!/usr/bin/env python

"""
This file is used to run the test script individually
Example:
python3 script/runtest.py -f testpacks/sd-wan/path_selection_application_aware_steering
 -c testpacks/sd-wan/testbed_lab/configuration.yaml -o result
"""
import os
import sys
import argparse
import ast
import yaml
import runpy
import logging
from test_framework.testbase.gen_testbed_config import *

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '-f', '--case', help='Test case configuration name, WITHOUT .yaml extension.')
arg_parser.add_argument(
    '-c', '--config', help='Testbed lab configuration file (YAML), testbed_map.py file also expected here mapping testcase to specific testbed.')
arg_parser.add_argument(
    '-o', '--outdir', help='Output result dir')

args = arg_parser.parse_args()
if args.case is None:
    sys.exit("Test case configuration file must be specified")
if args.config is None:
    sys.exit("Testbed lab configuration file (YAML) must be specified")
if args.outdir is None:
    sys.exit("Output dir must be specified")
args.input = args.case+'.yaml'

# Get test case ID, testbed name and script name
try:
    file_handle_tmp = open(args.input, encoding='utf-8')
    res = yaml.load(file_handle_tmp, Loader=yaml.FullLoader)
    testid = res['testcase']['id']
    testbed = res['testcase']['run_info']['testbed']
    scriptmodule = res['testcase']['run_info']['script_module']
    scriptclass = res['testcase']['run_info']['script_class']
except:
    sys.exit("Error in getting test case ID, testbed or script name")
finally:
    file_handle_tmp.close()

# Get test topology name
config_folder = args.outdir + '/' + testid
config_relative_location = testid + '/testbed.yaml'
config_location = args.outdir + '/' + testid + '/testbed.yaml'
mapfile = args.config[0:args.config.rfind('/')] + '/testbed_map.py'
map = runpy.run_path(mapfile)
topology = map['TESTCASE_TESTBEDS'][testid]

if not os.path.exists(args.config):
    sys.exit("Missing testbed config file: {0}".format(args.config))
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
if not os.path.exists(config_folder):
    os.mkdir(config_folder)
if not os.path.exists(args.input):
    sys.exit("Missing input testcase info file: {0}".format(args.input))

# Generate testbed yaml file
generate(args.config, testbed, topology, config_location)

class CaseInfo():
    '''For the test case information'''
    def __init__(self, testbed, outdir, inputfile):
        self.testbed = testbed
        self.outdir = outdir
        try:
            file_handle_tmp = open(inputfile, encoding='utf-8')
            res = yaml.load(file_handle_tmp, Loader=yaml.FullLoader)
            self.testcase_id = res['testcase']['id']
            self.script_module = res['testcase']['run_info']['script_module']
            self.sne_config_file = res['testcase']['run_info'].get('sne_config_file')
        except:
            sys.exit("Error when creatting the class caseinfo")
        finally:
            file_handle_tmp.close()

info = CaseInfo(config_relative_location, args.outdir, args.input)

class_name = scriptclass 

exec("run_class = __import__('{0}', fromlist=('{1}'))".format(scriptmodule, class_name))

print("<--------test initializing...----------->")
exec("runner = run_class.{0}(info)".format(class_name))
try:
    print("<--------test setup...------------------>")
    runner.logger.setLevel(logging.DEBUG)
    runner.setup()
    print("<--------test run...-------------------->")
    runner.run()
    print("<------------test pass------------------>")
except Exception as exce:
    print("Error: %s" % exce)
finally:
    print("<--------test cleanup...---------------->")
    runner.cleanup()
    print("<--------test end----------------------->")
