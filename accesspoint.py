# -*- coding: utf-8 -*-
import os
import subprocess
import time
from constants import *


class AccessPoint:
    def __init__(self):
        self.interface = None
        self.internet_interface = None
        self.channel = None
        self.essid = None
        self.psk = None

    def set_interface(self, interface):
        self.interface = interface

    def set_internet_interface(self, interface):
        self.internet_interface = interface

    def set_channel(self, channel):
        self.channel = channel

    def set_essid(self, essid):
        self.essid = essid

    def set_psk(self, psk):
        self.psk = psk

    def start_dhcp_dns(self):

        config = (
            'no-resolv\n'
            'interface=%s\n'
            'dhcp-range=%s\n'
        )

        with open('/tmp/dhcpd.conf', 'w') as dhcpconf:
            dhcpconf.write(config % (self.interface, DHCP_LEASE))

        with open('/tmp/dhcpd.conf', 'a+') as dhcpconf:
            if self.internet_interface:
                dhcpconf.write("server=%s" % (PUBLIC_DNS,))
            else:
                dhcpconf.write("address=/#/%s" % (NETWORK_GW_IP,))

        dhcp = subprocess.Popen(['dnsmasq', '-C', '/tmp/dhcpd.conf'], stdout=DN, stderr=ER)
        time.sleep(1)
        try:
            if dhcp.poll() is None:
                print('[' + R + '+' + W +
                      '] Ошибка при запуске DHCP(DNS) сервера.\n' +
                      '[' + R + '+' + W +
                      '] Попробуйте перезапустить модуль.'
                      )
                raise Exception
        except KeyboardInterrupt:
            raise Exception
        subprocess.Popen(['ifconfig', str(self.interface), 'mtu', '1400'], stdout=DN, stderr=ER)
        subprocess.Popen(
            ['ifconfig', str(self.interface), 'up', NETWORK_GW_IP,
             'netmask', NETWORK_MASK
             ],
            stdout=DN,
            stderr=ER
        )
        # Give it some time to avoid "SIOCADDRT: Network is unreachable"
        time.sleep(.5)
        # Make sure that we have set the network properly.
        proc = str(subprocess.check_output(['ifconfig', str(self.interface)]))
        if proc.find(NETWORK_GW_IP) == -1:
            return False
        subprocess.call(
            ('route add -net %s netmask %s gw %s' %
             (NETWORK_IP, NETWORK_MASK, NETWORK_GW_IP)),
            shell=True)

    def start(self):
        config = (
            'interface=%s\n'
            'driver=nl80211\n'
            'ssid=%s\n'
            'hw_mode=g\n'
            'channel=%s\n'
            'macaddr_acl=0\n'
            'ignore_broadcast_ssid=0\n'
        )
        if self.psk:
            config += (
                          'wpa=2\n'
                          'wpa_passphrase=%s\n'
                      ) % self.psk

        with open('/tmp/hostapd.conf', 'w') as conf:
            conf.write(config % (self.interface, self.essid, self.channel))

        hostapd_proc = subprocess.Popen(['hostapd', '/tmp/hostapd.conf'],
                                        stdout=DN, stderr=ER)
        try:
            time.sleep(2)
            if hostapd_proc.poll() is not None:
                # hostapd will exit on error
                print('[' + R + '+' + W +
                      '] Failed to start access point! (hostapd error)\n' +
                      '[' + R + '+' + W +
                      '] Try a different wireless interface using -aI option.'
                      )
                raise Exception
        except KeyboardInterrupt:
            raise Exception

    @staticmethod
    def set_ip_fwd():
        subprocess.Popen(
            ['sysctl', '-w', 'net.ipv4.ip_forward=1'], stdout=DN, stderr=ER)

    @staticmethod
    def set_route_localnet():
        subprocess.Popen(
            ['sysctl', '-w', 'net.ipv4.conf.all.route_localnet=1'], stdout=DN, stderr=ER)

    @staticmethod
    def on_exit():
        subprocess.call('pkill dnsmasq', shell=True)
        subprocess.call('pkill hostapd', shell=True)

        if os.path.isfile('/tmp/hostapd.conf'):
            os.remove('/tmp/hostapd.conf')
        if os.path.isfile('/var/lib/misc/dnsmasq.leases'):
            os.remove('/var/lib/misc/dnsmasq.leases')
        if os.path.isfile('/tmp/dhcpd.conf'):
            os.remove('/tmp/dhcpd.conf')
