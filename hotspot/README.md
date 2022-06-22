# Raspberry Pi Hotspot

This is a guide on how to setup a WiFi hotspot on a Raspberry Pi. It is useful in the STF setup, as it can grant internet access to the phones. Furthermore, if you want to follow the [devices-ondemand](devices-ondemand/README.md) guide, then you can also connect the Smart Plug involved in this hotspot.

This guide is heavily based on the a great guide from [here](https://raspberrypi-guide.github.io/networking/create-wireless-access-point).

## Hotspot creation

We will configure the Pi to manage the IP range `192.168.40.0/24`. More specifically, the Pi will act as the gateway and have IP address `192.168.40.1`, and the clients of the network will be given IP addresses in range `[192.168.40.2, 192.168.40.254]`.

First, install DNSMasq and HostAPD:

```bash
sudo apt install -y dnsmasq hostapd
```

Next, stop the installed services so we can modify their configuration:

```bash
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
```

Modify /etc/dhcpcd.conf and append the following lines at the end of the file:

```txt
interface wlan0
    static ip_address=192.168.40.1/24
    nohook wpa_supplicant
```

Modify /etc/dnsmasq.conf and append the following lines at the end of the file:

```txt
interface=wlan0
dhcp-range=192.168.40.2,192.168.40.254,255.255.255.0,24h
```

Create the file /etc/hostapd/hostapd.conf:

```txt
wget https://raw.githubusercontent.com/S2-group/energy-experiments-utilities/master/hotspot/hostapd.conf
sudo mv hostapd.conf /etc/hostapd/hostapd.conf
```

Modify the newly created /etc/hostapd/hostapd.conf, and change the `ssid`, `country_code`, and `wpa_passphrase` to your liking.

Modify the file /etc/default/hostapd and find the line `#DAEMON_CONF`. Replace it with:

```txt
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

Enable hostapd to start automatically upon boot:

```bash
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```

Finally, start all the configured services:

```bash
sudo service dhcpcd restart
sudo systemctl start dnsmasq
sudo systemctl start hostapd
```

### Testing

To verify that the hotspot works, try connecting to it from your mobile device.

## Accessing main network from hotspot

Now, we will configure the Pi so that the main network, is accessible from devices in the hotspot. This will allow the phones to connect to the internet.

First, install `iptables-persistent` and click "Yes" on the prompts:

```bash
sudo apt install iptables-persistent
```

Modify /etc/sysctl.conf and uncomment the following line:

```txt
net.ipv4.ip_forward=1
```

Next, add the following iptables rule:

```bash
sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
```

Make the iptables change to persist across reboots:

```bash
sudo netfilter-persistent save
```

Finally, reboot the Pi. To verify that the whole hotspot setup works, try accessing any website from a device connected to the hotspot. Also try accessing a website from the Pi. Both should work.
