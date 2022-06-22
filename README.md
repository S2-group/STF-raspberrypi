# Energy Experiment Utilities

This is a repository containing information on how to run a [Smartphone Test Farm (STF)](https://github.com/DeviceFarmer/stf) on a Raspberry Pi Model 4B. 

Furthermore, it demonstrates a novel, low-cost, and creative approach to solve the common battery degradation problem [(issue#426)](https://github.com/openstf/stf/issues/426) faced by all STF users.

## Guides

1. [STF local development](STF.md) - A guide on how to setup a local development STF instance.
2. [STF production](STF-production/README.md) - A guide on how to move away from a local development STF instance, into deploying each STF component individually as in a [production environment](https://github.com/DeviceFarmer/stf/blob/master/doc/DEPLOYMENT.md).
3. [Devices on demand](devices-ondemand/README.md) - A guide on how to solve the [battery issue](https://github.com/openstf/stf/issues/426) for STF setups. It uses a smart plug and an externally powered USB hub to remotely **boot** and **power-off** phone devices.
4. [Hotspot](hotspot/README.md)  - A guide on how to setup the Pi's WiFi antenna to act as a hotspot. Useful for the phones to have internet access.

## Assumptions

The setup of STF has been tested on the following list of hardware and software assumptions. However, this does not mean that this guide is not applicable to other similar setups (e.g. older Pi models, 32-bit OS, etc.)

### Hardware Assumptions

* Raspberry Pi Model 4B.
* A **good quality SD card** that servers as the PI's OS is really important! This is to speed up the compilation and installation process, but most importantly to run the STF and have reasonably low latency when interacting with phones.
  * An SDXC (Speed) Class 10, UHS-1 (U1), V10 or better.<br /><img src="https://static1.anpoimages.com/wordpress/wp-content/uploads/2017/05/nexus2cee_video_speed-class_01.jpg" alt="SD speed classification" width="300"/>
  * Prefer reputable quality brands, such as Kingston, Samsung, SanDisk, etc.

### Software Assumptions

* Operating System: Raspberry PI OS (Raspbian) (64-bit) based on Debian bullseye.

### Additional System Information

This guide has been tested on a system with the following specifications:

```log
Raspberry Pi Model 4B

pi@raspberrypi:~ $ uname -a
Linux raspberrypi 5.15.32-v8+ #1538 SMP PREEMPT Thu Mar 31 19:40:39 BST 2022 aarch64 GNU/Linux

pi@raspberrypi:~ $ lsb_release -a
No LSB modules are available.
Distributor ID: Debian
Description:    Debian GNU/Linux 11 (bullseye)
Release:        11
Codename:       bullseye
```
