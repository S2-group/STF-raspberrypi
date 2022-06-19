
import logging
import subprocess
import shlex
import sys
import time
from tqdm import tqdm
from PyP100 import PyP100
from hubUtils import *

POWEROFF_DELAY=30 # in seconds
assert(POWEROFF_DELAY >= 30) # assumption for the code bellow

# script delayed-poweroff.sh
#
# #!/system/bin/sh
# sleep 30
# setprop sys.powerctl shutdown,userrequested

if __name__ == "__main__":
    device_list = get_enabled_devices()

    if len(device_list) == 0:
        LOGGER.warning("No devices found!")
        sys.exit(0)
    
    p100 = PyP100.P100(TAPO_HOSTNAME, TAPO_EMAIL, TAPO_PASSWORD)
    p100.handshake()
    p100.login()

    if not p100.getDeviceInfo()['result']['device_on']:
        LOGGER.warning("HUB-PSU is already powered off!")
        sys.exit(0)

    backlog = []
    for device in device_list:
        device.run_adb_cmd('shell input keyevent KEYCODE_WAKEUP') # wakeup the device
        backlog.append(
            device.async_adb_cmd('shell "cd /storage/self/primary/scripts/ && nohup sh ./delayed-poweroff.sh </dev/null &"') # power off the device
        )
        LOGGER.info('Shutdown command for device {} issued!'.format(device.serial))

    start = time.time()
    LOGGER.info('Waiting for HUB-PSU to power off...')

    time.sleep(10) # Give the adb shutdown commands enough time to be issued
    p100.turnOff()

    # wait until the commands return
    for p in backlog:
        LOGGER.debug('Waiting for command: {}'.format(' '.join(p.args)))
        LOGGER.debug(' [*] ...')
        try:
            p.wait(POWEROFF_DELAY-20)
        except subprocess.TimeoutExpired as e:
            LOGGER.error(" [*] ERROR! Command timed-out! Power supply was probably not cut-off in time!")
            LOGGER.error(" [*] There is a high chance that the device is still online!")
            LOGGER.error(" [*] Repeat the shutdown process!")
            sys.exit(1)

    LOGGER.info("HUB-PSU successfully powered off.")
    finish = time.time()
    delta = int(finish-start)
    remainder = max(0, POWEROFF_DELAY-delta)

    LOGGER.info("Waiting {} seconds for devices to shut down".format(remainder))
    for _ in tqdm(range(remainder)):
        time.sleep(1)

    LOGGER.info("SUCCESS!")
    sys.exit(0)



