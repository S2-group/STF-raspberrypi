

import time
import sys

from PyP100 import PyP100
from hubUtils import *

if __name__ == "__main__":

    LOGGER.info('Waiting for HUB-PSU to power on...')
    p100 = PyP100.P100(TAPO_HOSTNAME, TAPO_EMAIL, TAPO_PASSWORD)
    p100.handshake()
    p100.login()

    if p100.getDeviceInfo()['result']['device_on']:
        LOGGER.warning("HUB-PSU is already powered on")
        sys.exit(0)

    p100.turnOn()

    LOGGER.info("HUB-PSU successfully powered on.")
    LOGGER.info("Waiting for devices to appear under adb...")
    while len(get_enabled_devices()) == 0:
        time.sleep(4)

    LOGGER.info("Devices have booted!")
    print(get_enabled_devices())
    

