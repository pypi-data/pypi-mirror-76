# Genie extension
import genie.libs.conf.device.iosxe.device

def showlog(self):
    out = self.execute('show logging')
    return out

def config_interfaces(self):
    for intf in self.interfaces.values():
        intf.build_config()

genie.libs.conf.device.iosxe.device.Device.showlog = showlog
genie.libs.conf.device.iosxe.device.Device.config_interfaces = config_interfaces
