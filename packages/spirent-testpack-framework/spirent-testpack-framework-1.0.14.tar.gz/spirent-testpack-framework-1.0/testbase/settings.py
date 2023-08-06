"""
Define constant variable
"""

import os
import sys

SPIRENT_OS = 'spirent'
SNE_TYPE = 'sne'
STC_TYPE = 'stc'
STC_PORTLIST_TYPE = 'stc_portlist'
SNE_MAP_NAME = 'snemap_testpack'
SNE_CONFIG_FILE = sys.path[0] + '/sneConfig.xml'
SNE_CLI_COMMAND_DELAY = 5
STC_DEVICE_CREATE_ARGS = ['Port', 'IfCount', 'IfStack', 'DeviceCount', 'LoopbackIf', 'DeviceType', 'DeviceTags', 'DeviceRole', 'CreateCount', 'AffiliatedDevice']
STC_DEVICE_CONFIG_ARGS = ['Name', 'EnablePingResponse', 'RouterId', 'RouterIdStep', 'Ipv6RouterId', 'Ipv6RouterIdStep']
STC_IF_NAME = ['Ipv4If', 'Ipv6If', 'VlanIf', 'EthIIIf']
SNE_OBJECT = 'sne'
STC_OBJECT = 'stc'
LABSERVER_OBJECT = 'lab_server'
TESTBED_OBJECT = 'testbed'
