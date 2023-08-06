"""
Basic BGP test on router
"""
import time

from genie.libs.conf.bgp import Bgp
from test_framework.testbase.testbase import TestBase

class BgpRoutesStability(TestBase):
    """
    Class to test BGP routes stability
    """
    def __init__(self, test_input):
        super().__init__(test_input)

        self.stc_bgp_stable = self.testbed.devices['stc_bgp_stable']
        self.stc_bgp_unstable = self.testbed.devices['stc_bgp_unstable']
        if self.stc_bgp_stable is None or self.stc_bgp_unstable is None:
            raise RuntimeError("Testbed config missing BGP device(s)")

        self.logger.info(self.stc_bgp_stable.custom.as_start)

        for iface in self.stc_bgp_stable.ports:
            self.logger.info(iface.name)

        for iface in self.stc_bgp_unstable.ports:
            self.logger.info(iface.name)

    def run(self):
        raise RuntimeError("Test under development")
