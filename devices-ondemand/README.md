# Devices - On Demand

This is a guide on how to configure your android devices to boot when plugged into a charger and power off after issuing a delayed shutdown command.

This guide can be combined with the STF in order to make the phone devices boot on demand and then have them available in STF. Once you are done with testing, you can power off the devices in order to avoid having them permanently charing and risking battery life ([issue#426](https://github.com/openstf/stf/issues/426)). Once the setup is complete, booting and powering off the phones can be done remotely.

## Assumptions

### Hardware Assumptions

* We assume that we have >= 1 phones which are connected to a USB hub that is drawing power externally (so not from the PI, but from its own PSU).
  * e.g. For this setup, we an used [Anker 10 Port 60W Data Hub](https://us.anker.com/products/a7515) which draws power form an external PSU.
* A good quality Smart Plug; meaning that it is reliable when reading its state, uses TLS, and there is some community project that provides support for scripting.
  * For this guide, we will assume [TP-Link Tapo P100](https://www.tp-link.com/en/home-networking/smart-plug/tapo-p100/) for which there is also a nice [python library to interact with it](https://github.com/fishbigger/TapoP100).
* The USB hub's power supply should be plugged into the the Smart Plug

## Phone setup

### Setting `off-mode-charge` OEM feature

In this section, we will setup a phone to power on when the charger gets plugged in. This has been tested with Google Pixel 3 and Google Pixel 5 and works. It was also testing on an LG Nexus 5X, but did not work. (Most likely all devices that feature Qualcomm SoC do not work with this approach.)

First, navigate in the Developer Options of your phone and enable [USB debugging](https://developer.android.com/studio/debug/dev-options#enable) and "OEM unlocking". Also navigate to Display --> Advanced --> Screen timeout --> and set it tou a value >= 1 minute. Next, connect your phone to the Pi and wait for it to appear under adb:

```bash
stf@raspberrypi:~ $ adb devices
List of devices attached
01fbbAAAAAAAAAAA        device
```

Then, reboot the device into bootloader mode:

```bash
adb reboot bootloader
```

Now the device should appear under fastboot:

```bash
stf@raspberrypi:~ $ sudo $(which fastboot) devices
01fbbAAAAAAAAAAA        fastboot
```

Finally, set the OEM setting which automatically turns on the phone when a power source is detected and then reboot:

```bash
sudo $(which fastboot) oem off-mode-charge 0
sudo $(which fastboot) reboot
```

*(N.B.: Not all manifacturers implement this setting or it might have a different name under different OEMs.)*

Now to test if this worked or not, unplug your phone and shut it off. If you plugin your charger, then your phone should boot.

### Creating delayed power-off script

Now, we will create a helper script inside the phone for the delayed power off. Connect to the phone via `adb shell` and enter the following commands

```bash
mkdir -p /storage/self/primary/scripts
cd /storage/self/primary/scripts
touch delayed-poweroff.sh
chmod ug+x delayed-poweroff.sh
cat > delayed-poweroff.sh
#!/system/bin/sh
sleep 30
setprop sys.powerctl shutdown,userrequested

```

and then hit `[CTRL+D]`. If you `cat delayed-poweroff.sh` then you should see the script.

Now, to verify that the script works, enter the following command and immediately disconnect your phone:

```bash
adb shell "cd /storage/self/primary/scripts/ && nohup sh ./delayed-poweroff.sh </dev/null &"
```

After about ~30 seconds, the device should automatically power off. Re-plugging the phone should automatically power it on.

## SmartPlug setup

The SmartPlug has no particular setup. It should only be accessible by the Pi in a local network. Ideally, the Pi is connected to the outside world via Ethernet, and you use its WiFi adapter to create a hotspot where both the phones and the Smart Plug connect to.

## Automation script setup

Now let's download and configure the automation scripts:

```bash
mkdir -p sources

git clone https://github.com/S2-group/energy-experiments-utilities.git
mv energy-experiments-utilities/devices-ondemand/sources/* sources
rm -rf energy-experiments-utilities
```

First install the python requirements:

```bash
pip install -r sources/requirements.txt
rm sources/requirements.txt
```

Next, modify sources/hubUtils.py and set `TAPO_HOSTNAME`, `TAPO_EMAIL`, and `TAPO_PASSWORD`.

### Workflow

At this point, everything has been configured. So, let's test the setup.

#### Shutting down phones

To shutdown the phones, enter the following commands:

```bash
cd sources
python hub-shutdown.py
```

and after ~30 seconds, the phones should have shut down. Here is what happens behind the scenes:

1. adb issues a delayed power off command to the phones (i.e. shut down after 30 seconds)
2. The Smart Plug gets powered off, which in turn cuts the power to the hub and thus to the phones.
3. The phones will automatically shutdown after the delay.

The reason that we use a delayed power off command is to avoid a chicken-and-egg problem: If you power off the phones instantly, then they will reboot as the hub still has power. If you power off the hub first, then the phones are no longer reachable as the USB hub appears disconnected in the Pi.

#### Booting up phones

To boot again the phones now, enter the following commands:

```bash
cd sources
python hub-start.py
```

and the phones should boot. They will also appear under STF, if you have it installed. Here is what happens behind the scenes:

1. The Smart Plug gets powered on. This will inturn power on the hub, which will in turn give power to the phones.
2. The phones detect a power source so they boot.
3. The hones appear under adb, and eventually under STF.

## Troubleshooting

* The troubleshooting of [STF](STF.md) and [STF production](STF-production/README.md) also apply
* Use `lsusb` to see if the Pi is detecting a phone or not
* Use [uhubctl](https://github.com/mvp/uhubctl) as a more fine-grained method to gather USB information.
  * Instructions:
    ```bash
    sudo apt install -y libusb-1.0-0-dev
    git clone https://github.com/mvp/uhubctl
    cd uhubctl
    make
    sudo make install
    cd ..
    rm -rf uhubctl
    ```
  * Usage: `sudo uhubctl`
* Make sure that phones are not password protect (Security --> Screen Lock --> OFF) or modify the automation scripts accordingly.
* The screen has to be on while the delayed-poweroff.sh script is running.