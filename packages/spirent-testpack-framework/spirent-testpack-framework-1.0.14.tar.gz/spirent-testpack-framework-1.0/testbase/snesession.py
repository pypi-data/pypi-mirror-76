"""
SneSession for SNE Session using Genie
"""
import test_framework.testbase.snedevice as snedevice
from test_framework.testbase.settings import *

class SneSession():

    """
    SNE Session using Genie
    """

    def __init__(self, sne_devices, logger, out_dir):
        """Initialize StcClient instance from testbed data."""
        self._logger = logger
        self.devices = {}

        if not sne_devices:
            raise RuntimeError("Missing sne device")

        for sne_device in sne_devices:
            self._logger.info(object=SNE_OBJECT, event="add_new_device", name=sne_device.name)
            self.devices[sne_device.name] = snedevice.SneDevice(sne_device, self._logger, out_dir)

    def end(self):
        '''sessoin end'''
        self._logger.info(object=SNE_OBJECT, event="session_end")
        for name in self.devices:
            self.devices[name].unload()
