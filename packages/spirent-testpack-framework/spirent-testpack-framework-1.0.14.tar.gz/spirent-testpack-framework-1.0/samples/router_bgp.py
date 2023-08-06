"""
Basic BGP test on router
"""
import time

from genie.libs.conf.bgp import Bgp
from test_framework.testbase.testbase import TestBase

class BasicBgp(TestBase):
    """
    Class to test basic BGP function of router
    """
    def __init__(self, test_input):
        super().__init__(test_input)
        self.dut = self.testbed.devices['dut1']

        self.port1 = self.stc.port("stc_port1")
        self.port2 = self.stc.port("stc_port2")
        if self.port1 is None or self.port2 is None:
            raise RuntimeError("Testbed config missing STC port(s)")

        self.bgp = None

    def setup(self):
        """
        Setup testbed
        """
        super().setup()

        self.logger.info("Connecting to DUT")
        self.dut.connect()

    def run(self):
        """
        Main test logic
        """
        logger = self.logger
        stc = self.stc
        project = stc.project()

        #################################################################################
        # Obtain port objects, create underlying phy ojects and configure relationships #
        #################################################################################
        port1_h = self.port1.handle

        phy_1 = stc.create(self.port1.stc_config['phy'], under=port1_h)
        stc.config(port1_h, {"ActivePhy-targets": phy_1})

        port2_h = self.port2.handle

        phy_2 = stc.create(self.port2.stc_config['phy'], under=port2_h)
        stc.config(port2_h, {"ActivePhy-targets": phy_2})

        #################################################################
        # Create Device Blocks, underlying interfaces and relationships #
        #################################################################
        logger.info("Creating Emulated Device Blocks")
        emulated_device_1 = stc.create("EmulatedDevice", under=project)
        ipv4_if_1 = stc.create("Ipv4If", under=emulated_device_1, Address=str(self.port1.ipv4.ip),
                               PrefixLength=self.port1.ipv4.network.prefixlen, Gateway=self.port1.gateway)
        eth_if_1 = stc.create("EthIIIf", under=emulated_device_1, SourceMac="00:00:00:00:00:01")
        stc.config(emulated_device_1, {"TopLevelIf-targets": [ipv4_if_1]})
        stc.config(emulated_device_1, {"PrimaryIf-targets": [ipv4_if_1]})
        stc.config(ipv4_if_1, {"StackedOnEndpoint-targets": [eth_if_1]})
        stc.config(port1_h, {"AffiliationPort-sources": [emulated_device_1]})

        emulated_device_2 = stc.create("EmulatedDevice", under=project)
        ipv4_if_2 = stc.create("Ipv4If", under=emulated_device_2, Address=str(self.port2.ipv4.ip),
                               PrefixLength=self.port2.ipv4.network.prefixlen, Gateway=self.port2.gateway)
        eth_if_2 = stc.create("EthIIIf", under=emulated_device_2, SourceMac="00:00:00:00:00:02")
        stc.config(emulated_device_2, {"TopLevelIf-targets": [ipv4_if_2]})
        stc.config(emulated_device_2, {"PrimaryIf-targets": [ipv4_if_2]})
        stc.config(ipv4_if_2, {"StackedOnEndpoint-targets": [eth_if_2]})
        stc.config(port2_h, {"AffiliationPort-sources": [emulated_device_2]})

        #########################################################################################################################
        # Create Bgpv4 Router and IPv4 route block configuration. Since unclear on the changes required to support adding       #
        # BGP information. So will configure the DUT to use interface address as the source-update address                      #
        #########################################################################################################################
        bgp_data = self.port2.bgp
        bgp_router_config_1 = stc.create("BgpRouterConfig", under=emulated_device_2, AsNum=bgp_data['as_num'],
                                         DutAsNum=bgp_data['dut_as_num'], UseGatewayAsDut=bgp_data['use_gateway_as_dut'])
        bgp_ipv4_route_config_1 = stc.create("BgpIpv4RouteConfig", under=bgp_router_config_1)
        ipv4_network_block_1 = (stc.get(bgp_ipv4_route_config_1, 'children-Ipv4NetworkBlock')).split(' ')[0]
        stc.config(ipv4_network_block_1, StartIpList="100.0.0.0", PrefixLength="24")

        #############################################################################################################
        # Create Stream Block and set bindings so traffic sources from emulated_device_1 and targets Bgp Route Block #
        #############################################################################################################
        logger.info('Creating StreamBlock on Port 1')
        stream_block = stc.create('streamBlock', under=port1_h)
        stc.config(stream_block, {"SrcBinding-targets": [ipv4_if_1]})
        stc.config(stream_block, {"DstBinding-targets": [ipv4_network_block_1]})

        # Apply test config
        stc.apply()

        logger.info("Configuring DUT interfaces")
        for intf in self.dut.interfaces.values():
            if intf.alias == 'port1':
                intf.ipv4 = "30.0.1.1/24"
            else:
                intf.ipv4 = "30.0.2.1/24"
            intf.build_config()

        logger.info("Configuring BGP")
        self.bgp = Bgp(asn=123)
        self.dut.add_feature(self.bgp)
        self.bgp.device_attr[self.dut].add_neighbor(self.port2.ipv4)

        try:
            self.bgp.build_config()
        except Exception as exce:
            logger.info(str(exce))
            raise

        ###############################################
        # Subscribe to generator and analyzer results #
        ###############################################
        logger.info('Subscribing to results')
        status = stc.perform('ResultsSubscribeCommand', Parent=project, ResultParent=port1_h,
                             ConfigType='Generator', resulttype='GeneratorPortResults',
                             filenameprefix='Generator_port1_counter')
        port1_generator_result = status['ReturnedDataSet']
        status = stc.perform('ResultsSubscribeCommand', Parent=project, ResultParent=port2_h,
                             ConfigType='Analyzer', resulttype='AnalyzerPortResults',
                             filenameprefix='Analyzer_port2_counter')
        port2_analyzer_result = status['ReturnedDataSet']


        ################################################################
        # Verify links, ARP and start devices to establish BGP session #
        ################################################################
        logger.info('Verifying Links')
        verify_phy_link_status = stc.perform('PhyVerifyLinkUpCommand', PortList=project)
        if verify_phy_link_status['PassFailState'] != 'PASSED':
            raise RuntimeError("Error - One or more emulated devices failed to successfully ARP the DUT")

        logger.info('Performing ARP')
        arp_nd_status = stc.perform('ArpNdStartOnAllDevicesCommand', PortList=project, WaitForArpToFinish="TRUE")
        if arp_nd_status['ArpNdState'] != 'SUCCESSFUL':
            raise RuntimeError("Error - One or more emulated devices failed to successfully ARP the DUT")

        logger.info('Starting All Devices')
        devices_start_all_status = stc.perform('DevicesStartAllCommand', Project=project)
        if devices_start_all_status['Status'] != 'Start All Devices is successful':
            raise RuntimeError("Error starting all devices")

        logger.info('Waiting for Router to reach ESTABLISHED state')
        wait_for_router_state_status = stc.perform('WaitForRouterStateCommand', ObjectList=[port1_h, port2_h])
        if wait_for_router_state_status['PassFailState'] != 'PASSED':
            raise RuntimeError("Error -  Bgp router failed to reach ESTABLISHEMENT state")

        logger.info('Waiting for Router to advertise all routes')
        wait_for_router_events_status = stc.perform('WaitForRoutingEventsCommand', PortList=port2_h)
        if wait_for_router_events_status['Status'] != 'Routing Events done.':
            raise RuntimeError("Error advertising BGP routes")

        ################################################################################
        # Send test traffic and verify that the DUT forwarded all packets with no loss #
        ################################################################################

        ########################
        # Configure generators #
        ########################
        logger.info("Configuring port1 generator")
        generator1 = stc.get(port1_h, 'children-Generator').split(' ')[0]
        generator_config1 = (stc.get(generator1, 'children-GeneratorConfig')).split(' ')[0]
        stc.config(generator_config1,
                   SchedulingMode="PORT_BASED",
                   Duration="60",
                   DurationMode="SECONDS",
                   BurstSize="1",
                   LoadUnit="PERCENT_LINE_RATE",
                   LoadMode="FIXED",
                   FixedLoad="10")

        #################################
        # Apply generator configuration #
        #################################
        logger.info("Applying generator configuration")
        stc.apply()

        #################
        # Start traffic #
        #################
        logger.info("Starting Traffic and wait for generator to stop")
        stc.perform('GeneratorStartCommand', GeneratorList=generator1)
        stc.perform('GeneratorWaitForStopCommand', GeneratorList=generator1, WaitTimeout="90")
        logger.info('sleeping for 5 seconds after generator stopped for residual traffic to get forwarded')
        time.sleep(5)

        #####################################################
        # Collect Tx Signature Frame and Rx Sig Frame Count #
        #####################################################
        gen_result = (stc.get(port1_generator_result, 'ResultHandleList')).split(' ')[0]
        tx_sig_count = stc.get(gen_result, 'GeneratorSigFrameCount')
        analyzer_result = stc.get(port2_analyzer_result, 'ResultHandleList').split(' ')[0]
        rx_sig_count = stc.get(analyzer_result, 'SigFrameCount')

        if int(tx_sig_count) == int(rx_sig_count):
            msg = ''.join(['No Frame Loss Detected: TxFrameCount = ', str(tx_sig_count), ', RxFrameCount = ', str(rx_sig_count)])
            logger.info(msg)
            return msg
        else:
            loss = int(tx_sig_count) - int(rx_sig_count)
            msg = ''.join(['Frame Loss Detected: ', 'TxFrameCount = ', str(tx_sig_count), ', RxFrameCount = ', str(rx_sig_count),
                           ', Frame Loss = ' + str(loss)])
            logger.info(msg)
            raise RuntimeError(msg)

    def cleanup(self):
        try:
            # TODO the following code shuts down the ports - check Genie docs on how to avoid that
            #for intf in dut.interfaces.values():
                #intf.shutdown = False
                #intf.build_unconfig()

            #if self.bgp is not None:
                #self.bgp.build_unconfig()

            self.dut.disconnect()
        except Exception as exce:
            self.logger.warning("DUT unconfigure: %s" % (str(exce)))

        super().cleanup()
