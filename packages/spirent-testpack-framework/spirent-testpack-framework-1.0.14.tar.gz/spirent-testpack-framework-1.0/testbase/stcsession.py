"""
STC adapater for configure STC using REST API
"""
import getpass
import os
import time

from stcrestclient import stchttp
from test_framework.testbase.settings import *
from genie.libs.conf.interface.spirent import Interface

LS_SERVER_TYPE = 'stc_lab_server'
STC_PORT_TYPE = 'stc_port'

class StcSession():

    """
    Spirent TestCenter ReST Session from pyATS topology.

    """

    def __init__(self, testbed, logger, session_name="", user_name="", debug_level=0):
        """Initialize StcClient instance from testbed data."""

        self._logger = logger
        self._stc = None
        self._csp_port_map = {}
        self._name_port_map = {}
        self._project = None

        self._logger.debug("Enter StcSession.init()")

        self._ls_addr = None
        for server in testbed.servers.values():
            if server.type == LS_SERVER_TYPE:
                self._ls_addr = server.address
                break

        if not self._ls_addr:
            raise RuntimeError("testbed missing lab server")

        # Device(s) with variable list of ports which have to be added dynamically
        stc_portlist_devices = testbed.find_devices(os=SPIRENT_OS, type=STC_PORTLIST_TYPE)
        for dev in stc_portlist_devices:
            dev.ports = []
            i = 0
            for chassis in dev.custom.chassis_ports:
                chassis_ip = chassis['chassis']
                ports = chassis['ports']
                for slot_port in ports:
                    # The interface name is initially set to slot/port in order to use the
                    # parse method. But we have to set it to a unique value before adding to
                    # device, so that same slot / port from different chassis don't get overwritten.
                    iface = Interface(name=slot_port, type = 'ethernet')
                    parsed_iface = iface.parse_interface_name()
                    csp = "//%s/%s/%s" % (chassis_ip, parsed_iface.slot, parsed_iface.port)
                    if csp in self._csp_port_map:
                        raise RuntimeError("duplicate ports %s" % csp)
                    iface.name = csp
                    iface.location = csp
                    iface.handle = None
                    iface.device = dev

                    iface_name = dev.name + ".port" + str(i)
                    self._csp_port_map[csp] = iface
                    self._name_port_map[iface_name] = iface
                    dev.ports.append(iface)
                    i += 1

        stc_devices = testbed.find_devices(os=SPIRENT_OS, type=STC_TYPE)
        if not stc_devices and not stc_portlist_devices:
            raise RuntimeError("testbed missing stc")

        for stc_device in stc_devices:
            ifaces = stc_device.interfaces
            for iface in ifaces.values():
                if iface.type != STC_PORT_TYPE:
                    continue

                chassis = iface.chassis
                parsed_iface = iface.parse_interface_name()
                csp = "//%s/%s/%s" % (chassis, parsed_iface.slot, parsed_iface.port)
                if csp in self._csp_port_map:
                    raise RuntimeError("duplicate ports %s" % csp)

                iface.location = csp
                iface.handle = None

                self._csp_port_map[csp] = iface
                self._name_port_map[stc_device.name] = iface

        if not session_name:
            session_name = testbed.name

        self._user_name = user_name
        self._session_name = session_name
        self._dbg_level = debug_level

    def __getattr__(self, name):
        # Forward any attributes provided by stchttp.StcHttp
        if self._stc is None:
            raise RuntimeError("not started")
        return getattr(self._stc, name)

    def __str__(self):
        # String a line with csp + interface name for each port
        strs = []
        for csp, port in self._csp_port_map.items():
            strs.append("%s (%s)" % (csp, port.alias))

        strs.sort()
        return '\n'.join(strs)

    def start(self):
        """Start test session and connect to all STC ports in testbed

        The session that is created is named with the session name and the user
        name separated with ' - '.

        """
        self._logger.debug("Enter StcSession.start()", object=STC_OBJECT, event="start_session")

        if self._stc is not None:
            raise RuntimeError("already started")

        # Connect to lab server
        stc = stchttp.StcHttp(self._ls_addr, debug_print=bool(self._dbg_level > 1))

        # Create new test session
        user_name = self._user_name

        # If user name not specified, try to get the name of the current user.
        if not user_name:
            try:
                user_name = getpass.getuser()
            except:
                pass

        if self._dbg_level:
            self._logger.info(object=STC_OBJECT, event="start_new_session", name=self._session_name)

        stc.new_session(user_name, self._session_name, True)
        self._logger.info(object=LABSERVER_OBJECT, stc_version=stc.bll_version())
        self._stc = stc

        try:
            # Create project
            self._project = stc.create('project')

            # Create and reserve all ports.
            stc_ports = []
            for port in self._name_port_map.values():
                csp = port.location
                if self._dbg_level:
                    self._logger.info(object=STC_OBJECT, event="create_port", address=csp)
                port.handle = stc.create('port', self._project, location=csp)
                stc_ports.append(port.handle)

            # Connect, reserve and map ports
            if self._dbg_level:
                self._logger.info(object=STC_OBJECT, event="attach_port", ports=stc_ports)
            self._logger.console("Attaching stc ports...")
            stc.perform('AttachPorts', portList=stc_ports, autoConnect='TRUE')
            self._logger.console("done\n")

        except Exception:
            self.end()
            raise

        if self._dbg_level:
            self._logger.info(object=LABSERVER_OBJECT, event="started_session", name=stc.session_id())
            sys_info = stc.system_info()
            del sys_info['supported_api_versions']
            for key, value in sys_info.items():
                self._logger.info({key:value})


    def end(self):
        """Release ports and terminate test session"""
        if self._stc is None:
            self._logger.info("STC session not started")
            return

        # Release all ports.
        for port in self._name_port_map.values():
            if not port.handle:
                continue
            csp = port.location
            if self._dbg_level:
                self._logger.info(object=STC_OBJECT, event="release_port", address=csp)
            try:
                self._stc.perform('releasePort', location=csp)
            except Exception as excep:
                self._logger.error(object=STC_OBJECT, event="release_port", address=csp, exception=str(excep))
            del port.handle

        # Disconnect all chassis and end test session.
        if self._dbg_level:
            self._logger.info(object=STC_OBJECT, event="disconnect_all_chassis")
        try:
            self._stc.disconnectall()
        except Exception as excep:
            self._logger.error(object=STC_OBJECT, event="disconnect_chassis", exception=str(excep))

        self._stc.end_session()
        if self._dbg_level:
            self._logger.info(object=STC_OBJECT, event="ended_session")

        self._stc = None

    def ls_address(self):
        """Return the Lab Server address"""
        return self._ls_addr

    def ports(self):
        """Return a slice of port dicts"""
        return [port for port in self._name_port_map.values()]

    def port(self, name):
        """Lookup information for a port by its stc port number.

        If port is connected/reserved, then 'handle' key has a value.

        """
        return self._name_port_map.get(name)

    def sne_port(self, name):
        """Lookup information for a SNE port by its alias.

        """
        return self._sne_port_map.get(name)
    @staticmethod
    def split_csp(csp):
        """Split a port location (//c/s/p) into chassis, slot, and port.

        Slot and port are returned as ints.

        """
        chassis, slot, port = csp.strip('/').split('/')
        return chassis, int(slot), int(port)

    def started(self):
        """Return True is test session started"""
        return bool(self._stc)

    def project(self):
        """Return the STC project"""
        return self._project

    def download_all_files(self, test_out_dir):
        """Download STC files(BLL/IL Logs, configuration file...)"""
        if os.path.exists(test_out_dir):
            self._stc.perform('GetEquipmentLogsCommand', {'EquipmentList': self._project})
            self._logger.info(object=STC_OBJECT, event="download_all_files")
            self._stc.download_all(dst_dir=test_out_dir)
        else:
            raise Exception("Destination directory: %s is not existing" % test_out_dir)

    def device_config(self, **args):
        """Config device"""
        device_create_args = {}
        device_config_args = {}
        if_args = {}
        for key, value in args.items():
            if key in STC_DEVICE_CREATE_ARGS:
                device_create_args[key] = value
            elif key in STC_DEVICE_CONFIG_ARGS:
                device_config_args[key] = value
            elif key in STC_IF_NAME:
                if_args[key] = value

        device = self._stc.perform('DeviceCreateCommand', ParentList=self._project, **device_create_args)

        if device_config_args:
            self._stc.config(device['ReturnList'], **device_config_args)

        if if_args:
            router = device['ReturnList']
            ethiiif = self._stc.get(device['ReturnList'], 'children-ethiiif')
            #TO do: only support the interface types in STC_IF_NAME, to support other types, need add them in STC_IF_NAME
            for name, value in if_args.items():
                if device_create_args['IfStack'].find(name) != -1:
                    stack_if = self._stc.get(device['ReturnList'], 'children-'+name)
                    if name.lower() == 'vlanif':
                        stack_if_list = stack_if.split(" ")
                        stack_length = len(stack_if_list)
                        for i in range(stack_length):
                            # vlanid1 : svlan, vlanid2 : cvlan, but in data model, the first vlan_if is cvlan_if
                            self._stc.config(stack_if_list[i], value[stack_length - 1 - i])
                    elif name.lower() == 'ipv4if':
                        self._stc.config(stack_if, {'toplevelif-Sources': router})
                        self._stc.config(stack_if, value)
                    elif name.lower() == 'ipv6if':
                        self._stc.config(stack_if, {"stackedonendpoint-Targets": ethiiif})
                        self._stc.config(stack_if, value)
                        # create new ipv6if for link-local address to fulfill ipv6 emulated device
                        ipv6if_link_local = self._stc.create('ipv6if', under=router)
                        self._stc.config(ipv6if_link_local, {'toplevelif-Sources': router})
                        if "VlanIf" in if_args:
                            # the last vlan-if is svlan-if, it should be as stackonendpoint-targets, if no svlan-if, use the cvlan-if
                            self._stc.config(ipv6if_link_local, {'stackedonendpoint-Targets': self._stc.get(router, 'children-vlanif').split(" ")[-1]})
                        self._stc.config(ipv6if_link_local, {'Address': 'fe80::1'})
                        self._stc.config(stack_if, value)
            if "VlanIf" in if_args:
                self._stc.config(ethiiif, {'stackedonendpoint-Sources': self._stc.get(router, 'children-vlanif').split(" ")[-1]})
            else:
                ipv4_if = self._stc.get(router, 'children-ipv4if')
                ipv6_if = self._stc.get(router, 'children-ipv6if')
                self._stc.config(ethiiif, {"stackedonendpoint-Sources": ipv4_if + " " + ipv6_if})

        return device

    def config_port(self, port, **args):
        """ config port properties: phy, speed, auto_negotiation """
        port_name = self._stc.get(port, 'Name')
        phy = ''
        speed = ''
        auto_nego = ''
        for key, value in args.items():
            if key == 'phy':
                phy = value
            elif key == 'speed':
                speed = value
            elif key == 'auto_negotiation':
                auto_nego = value
        if phy not in ('None', ''):
            self._logger.info(object=STC_OBJECT, event="config_phy", port_name=port_name)
            port_phy = self._stc.create(phy, under=port, attributes={'Name': port_name})
            self._stc.config(port, {"ActivePhy-targets": port_phy})
        else:
            self._logger.info(object=STC_OBJECT, event="search_phy", port_name=port_name)
            port_phy = self._stc.get(port, 'ActivePhy')
        if speed not in ('None', ''):
            self._logger.info(object=STC_OBJECT, event="config_speed", port_name=port_name, speed=speed)
            self._stc.config(port_phy, {"LineSpeed": speed})
        if auto_nego not in ('None', ''):
            self._logger.info(object=STC_OBJECT, event="config_auto_negotiation", port_name=port_name, auto_negotiation=auto_nego)
            self._stc.config(port_phy, {"AutoNegotiation": auto_nego})
        flag_verify_link = self._stc.perform('PhyVerifyLinkUp', portList=port)['PassFailState']
        if flag_verify_link != 'PASSED':
            raise Exception("Link status is down for port %s, please check the testbed and then re-run." % self._stc.get(port, 'Location'))

    def get_port_type(self, location, **args):
        target_name = location.split('/')[2]
        chassis_manager = self._stc.get('system1', 'children-physicalchassismanager')
        chassis_list = self._stc.get(chassis_manager, 'children-physicalchassis').split(' ')
        target_chassis = chassis_list[0]
        for chassis in chassis_list:
            chassis_name = self._stc.get(chassis, 'HostName')
            if chassis_name == target_name:
                target_chassis = chassis
        ptm_list = self._stc.get(target_chassis, 'children-physicaltestmodule').split(' ')
        # find target chassis and get module list
        for ptm in ptm_list:
            pg_list = self._stc.get(ptm, 'children-physicalportgroup').split(' ')
            for pg in pg_list:
                port_list = self._stc.get(pg, 'children-physicalport').split(' ')
                for port in port_list:
                    location_temp = self._stc.get(port, 'location')
                    if location_temp == location:
                        type = self._stc.get(pg, 'type')
                        return type
