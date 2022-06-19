
import logging
import subprocess
import shlex

TAPO_HOSTNAME="<REDACTED>"  # local IP or domain name of the smart plug. For TP-Link P100, "Tapo_SmartPlug" value also works.
TAPO_EMAIL="<REDACTED>"     # e.g. admin@admin.com
TAPO_PASSWORD="<REDACTED>"  # e.g. admin1234

logging.basicConfig()
LOGGER = logging.getLogger('HUB-PSU')
LOGGER.setLevel(logging.INFO)
# LOGGER.setLevel(logging.DEBUG)

class Device:
    def __init__(self, serial, state):
        self.serial = serial # case sensitive
        self.state = state.lower()
    
    def __repr__(self):
        return self.serial + "\t" + self.state
    
    def run_adb_cmd(self, cmd):
        res = subprocess.run(shlex.split('adb -s {} {}'.format(self.serial, cmd)), capture_output=True, check=True)
        LOGGER.debug(res)
        return res

    def async_adb_cmd(self, cmd):
        p = subprocess.Popen(
            shlex.split('adb -s {} {}'.format(self.serial, cmd)),
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        LOGGER.debug("Launched: {}".format(p))
        return p


def adb_get_devices():
    res = subprocess.run(['adb', 'devices'], capture_output=True, check=True)
    lines = res.stdout.decode('ascii').strip().split('\n')[1:]
    return [Device(*l.split('\t')) for l in lines]

def get_serial_blacklist():
    # Case sensitive list of serial numbers to blacklist so that they do not get processed by the script
    # e.g. "01fbbAAAAAAAAAAA"
    return [ ]

def get_enabled_devices():
    return list(filter(
        lambda dev: dev.state == "device" and dev.serial not in get_serial_blacklist(),
        adb_get_devices()
    ))
