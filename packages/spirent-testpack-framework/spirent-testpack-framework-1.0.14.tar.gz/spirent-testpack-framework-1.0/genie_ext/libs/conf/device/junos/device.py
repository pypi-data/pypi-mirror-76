'''
Device class for devices with junos OS.
'''

__all__ = (
    'Device',
)

from enum import Enum
import logging
import re
import telnetlib

from genie.decorator import managedattribute
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

import genie.libs.conf.device

from jnpr.junos import Device as junosDev
from jnpr.junos.utils.start_shell import StartShell

class Device(genie.libs.conf.device.Device):
    '''Device class for devices with junos OS'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telnet = None
        self.ssh = None

    def connect(self):
        host_ip = str(self.connections['a'].ip)
        username = self.tacacs['username']
        pwd = self.passwords['tacacs']

        proto = str(self.connections['a'].protocol)

        try:
            if proto == 'telnet':
                tn = telnetlib.Telnet(host)
                tn.read_until(b"login: ", timeout=60)
                _tn_writeln(tn, username)
                tn.read_until(b"Password: ", timeout=60)
                _tn_writeln(tn, pwd)
                self.telnet = tn
            elif proto == 'ssh':
                ss = StartShell(junosDev(host=host_ip, user=username, passwd=pwd))
                ss.open()
                self.ssh = ss
            else:
                raise RuntimeError("\nError connecting to junos device - unsupported protocol {}!".format(proto))
        except Exception as err:
            raise RuntimeError("\nError connecting to junos device - {}!".format(err))

    def disconnect(self):
        if self.telnet is not None:
            _tn_writeln(self.telnet, "exit")
        elif self.ssh is not None:
            self.ssh.close()

    def showlog(self):
        if self.ssh is not None:
            return self.ssh.run('cli -c "show log | no-more"')

    def switch_routing_engines(self):
        if self.ssh is not None:
            return self.ssh.run('cli -c "request chassis routing-engine master switch;yes"')

    def config_interfaces(self):
        if self.telnet is not None:
            _tn_writeln(self.telnet, "configure")

            for intf in self.interfaces.values():
                w = ''.join(["set interfaces ", intf.type, " unit 0 family inet address ", str(intf.ipv4)])
                _tn_writeln(self.telnet, w)

            _tn_writeln(self.telnet, "commit")
        elif self.ssh is not None:
            # Refer https://forums.juniper.net/t5/Ethernet-Switching/multiple-Junos-cli-commands-at-the-same-time/td-p/468323
            cmds = ["configure; "]

            for intf in self.interfaces.values():
                cmds.append(''.join(["set interfaces ", intf.type, " unit 0 family inet address ", str(intf.ipv4), "| no-more; "]))

            cmds.append("commit")
            cmd = ''.join(cmds)
            return self.ssh.run("cli -c '{}'".format(cmd))

def _tn_writeln(tn, w):
    tn.write(w.encode('ascii') + b"\n")
