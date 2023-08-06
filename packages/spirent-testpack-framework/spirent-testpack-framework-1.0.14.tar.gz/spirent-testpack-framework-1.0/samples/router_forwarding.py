"""
Basic router forwarding test
"""
import time
import test_framework.genie_ext

from test_framework.testbase.testbase import TestBase

#############################################################################
# Sample python TestCenter script to perform a two port test on a DUT. The  #
# test sends unidirection traffic and verifies the DUT forwards all packets.#
#############################################################################

class BasicForwarding(TestBase):
    """
    Class to test basic router forwading function
    """
    def __init__(self, test_input):
        super().__init__(test_input)
        self.dut = self.testbed.devices['dut1']
        self.logger.info("DUT class {}".format(self.dut.__class__.__module__ + '.' + self.dut.__class__.__name__))

        self.port1 = self.stc.port("stc_port1")
        self.port2 = self.stc.port("stc_port2")
        if self.port1 is None or self.port2 is None:
            raise RuntimeError("Testbed config missing STC port(s)")

    def setup(self):
        """
        Setup testbed
        """
        super().setup()

        self.logger.info("Connecting to DUT")
        self.dut.connect()
        self.logger.info("Done")

    def run(self):
        """
        Main test logic
        """
        logger = self.logger
        stc = self.stc
        project = stc.project()

        port1_h = self.port1.handle

        phy_1 = stc.create(self.port1.stc_config['phy'], under=port1_h)
        stc.config(port1_h, {"ActivePhy-targets": phy_1})

        port2_h = self.port2.handle

        phy_2 = stc.create(self.port2.stc_config['phy'], under=port2_h)
        stc.config(port2_h, {"ActivePhy-targets": phy_2})

        # Create Device Blocks, underlying interfaces and relationships
        logger.info("Creating Host Device Blocks")
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

        # Create Stream Block and set bindings so traffic sources from emulated_device_1
        # and targets emulated_device_2
        logger.info("Creating StreamBlock on Port 1")
        stream_block = stc.create('streamBlock', under=port1_h)
        stc.config(stream_block, {"SrcBinding-targets": [ipv4_if_1]})
        stc.config(stream_block, {"DstBinding-targets": [ipv4_if_2]})

        # Apply test config
        stc.apply()

        logger.info("Configuring DUT")
        for intf in self.dut.interfaces.values():
            if intf.alias == 'port1':
                intf.ipv4 = "30.0.1.1/24"
            else:
                intf.ipv4 = "30.0.2.1/24"

        logger.info(self.dut.config_interfaces())

        # Subscribe to generator and analyzer results
        logger.info('Subscribing to results')
        status = stc.perform('ResultsSubscribeCommand', Parent=project, ResultParent=port1_h,
                             ConfigType='Generator', resulttype='GeneratorPortResults',
                             filenameprefix='Generator_port1_counter')
        port1_generator_result = status['ReturnedDataSet']
        status = stc.perform('ResultsSubscribeCommand', Parent=project, ResultParent=port2_h,
                             ConfigType='Analyzer', resulttype='AnalyzerPortResults',
                             filenameprefix='Analyzer_port2_counter')
        port2_analyzer_result = status['ReturnedDataSet']

        # Perform Arp on bound device blocks to resolve DUT mac addresses
        logger.info("Arping devices to resolve mac address")
        arp_cmd_status = stc.perform('ArpNdStartCommand', WaitForArpToFinish="TRUE", HandleList=project)
        if arp_cmd_status['ArpNdState'] != 'SUCCESSFUL':
            raise RuntimeError("Error - One or more emulated devices failed to successfully ARP the DUT")

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
        analyzerresult = stc.get(port2_analyzer_result, 'ResultHandleList').split(' ')[0]
        rx_sig_count = stc.get(analyzerresult, 'SigFrameCount')

        logger.info(self.dut.showlog())

        if int(tx_sig_count) == int(rx_sig_count):
            msg = ''.join(['No frame loss detected: TxFrameCount = ', str(tx_sig_count), ', RxFrameCount = ', str(rx_sig_count)])
            logger.info(msg)
            return msg
        else:
            loss = int(tx_sig_count) - int(rx_sig_count)
            msg = ''.join(['Frame loss detected: ', 'TxFrameCount = ', str(tx_sig_count), ', RxFrameCount = ', str(rx_sig_count),
                           ', Frame Loss = ' + str(loss)])
            raise RuntimeError(msg)

    def cleanup(self):
        try:
            # TODO the following code shuts down the ports - check Genie docs on how to avoid that
            #for intf in dut.interfaces.values():
                #intf.shutdown = False
                #intf.build_unconfig()

            self.logger.info("Disconnecting device")
            self.dut.disconnect()
        except Exception as exce:
            self.logger.warning("cleanup: %s" % (str(exce)))

        super().cleanup()
