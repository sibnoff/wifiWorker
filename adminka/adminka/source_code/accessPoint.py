#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import subprocess
import time
from adminka.source_code.constants import *
from adminka.source_code.firewall import Firewall
from adminka.source_code.logging import Logging


# from constants import *
# from firewall import Firewall
# from logging import Logging


class ClientStation:
    """Клиент точки доступа. Атрибуты:
        - MAC
        - curent_ip
        - info(результат работы nmap)
        - trusted_essids
        - nick"""

    def __init__(self, mac):
        self.mac = mac
        self.last_ip = ''
        self.nick = ''
        self.info = dict()
        self.trasted_essid = []

    def __str__(self):
        """Возвращает строку: MAC:current_ip:nick"""
        return 'mac:{}, ip:{}, nick:{}'.format(self.mac, self.ip, self.nick)

    def set_signal(self, signal):
        self.info['signal'] = signal

    def set_ip(self, ip):
        self.last_ip = ip

    def set_nick(self, nick):
        self.nick = nick

    def add_trasted_essid(self, essid):
        self.trasted_essid.append(essid)

    def get_full_info(self):
        info = ' mac:{}, ip:{}, nick:{}\n' \
               '\tдоверенные сети: {}\n' \
               '\tдополнительная информация: ' \
               '{}'.format(self.mac, self.last_ip, self.nick, self.trasted_essid, self.info)
        return info


class AccessPoint:
    def __init__(self):
        self.interface = None
        self.internet_interface = None
        self.channel = None
        self.essid = None
        self.psk = None
        self.log = Logging(LOGS_DIR_NAME + 'main.log')
        self.fw = Firewall()

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
            'log-queries\n'
        )

        with open('/tmp/dhcpd.conf', 'w') as dhcpconf:
            dhcpconf.write(config % (self.interface, DHCP_LEASE))

        with open('/tmp/dhcpd.conf', 'a+') as dhcpconf:
            if self.internet_interface:
                dhcpconf.write("server=%s" % (PUBLIC_DNS,))
            else:
                dhcpconf.write("address=/#/%s\n" % (NETWORK_GW_IP,))
        output = open(LOGS_DIR_NAME + 'dnsmasq.output', 'w')
        dhcp = subprocess.Popen(['dnsmasq', '-C', '/tmp/dhcpd.conf'], stdout=output, stderr=ER)
        time.sleep(1)
        try:
            if dhcp.poll() is None:
                self.log.write_log('DHCP_ER', 'Не удалось запустить DHCP/DNS сервер')
                raise Exception
        except KeyboardInterrupt:
            raise Exception
        subprocess.Popen(['ifconfig', str(self.interface), 'mtu', '1400'], stdout=DN, stderr=ER)
        subprocess.Popen(
            ['ifconfig', str(self.interface), 'up', NETWORK_GW_IP,
             'netmask', NETWORK_MASK], stdout=DN, stderr=ER
        )
        time.sleep(.5)
        proc = str(subprocess.check_output(['ifconfig', str(self.interface)]))
        if proc.find(NETWORK_GW_IP) == -1:
            self.log.write_log('DHCP_ER', 'Не удалось запустить DHCP/DNS сервер')
            return False
        subprocess.call(
            ('route add -net %s netmask %s gw %s' %
             (NETWORK_IP, NETWORK_MASK, NETWORK_GW_IP)),
            shell=True)

    def start(self):
        self.log.write_log('AP', 'Начинаем запуск ТД')
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
            config += ('wpa=2\n'
                       'wpa_passphrase=%s\n') % self.psk

        with open('/tmp/hostapd.conf', 'w') as conf:
            conf.write(config % (self.interface, self.essid, self.channel))
        output = open(LOGS_DIR_NAME + 'hostapd.output', 'w')
        hostapd_proc = subprocess.Popen(['hostapd', '/tmp/hostapd.conf'], stdout=output, stderr=ER)
        try:
            time.sleep(2)
            if hostapd_proc.poll() is not None:
                self.log.write_log('AP_ER', 'Не удалось запустить ТД')
                raise Exception
        except KeyboardInterrupt:
            raise Exception
        try:
            self.log.write_log('AP', 'Сервис hostapd запущен')
            self.start_dhcp_dns()
            self.log.write_log('AP', 'DHCP/DNS сервер запущен')
            self.fw.nat(self.interface, self.internet_interface)
            self.set_ip_fwd()
            self.set_route_localnet()
            self.log.write_log('AP', 'Добавлены правила маршрутизации в iptables')
            self.log.write_log('AP', 'ТД {} запущена на интерфейсе {}'.format(self.essid, self.interface))
            self.write_state()
        except Exception as ex:
            AccessPoint.on_exit()
            self.log.write_log('AP_ER', 'Не удалось запустить ТД')

    def write_state(self):
        f = open(STATES_DIR_NAME + 'hotspot.state', 'w')
        params = dict()
        params['state'] = 1
        params['host_iface'] = self.interface
        params['gate_iface'] = self.internet_interface
        params['essid'] = self.essid
        params['hs_security'] = 'wpa2'
        params['psk'] = self.psk
        params['channel'] = self.channel
        f.writelines(json.dumps(params))
        f.close()

    @staticmethod
    def read_state():
        f = open(STATES_DIR_NAME + 'hotspot.state', 'r')
        params = json.loads(f.readline())
        f.close()
        return params

    @staticmethod
    def set_ip_fwd():
        subprocess.Popen(
            ['sysctl', '-w', 'net.ipv4.ip_forward=1'], stdout=DN, stderr=ER)

    @staticmethod
    def set_route_localnet():
        subprocess.Popen(
            ['sysctl', '-w', 'net.ipv4.conf.all.route_localnet=1'], stdout=DN, stderr=ER)

    @staticmethod
    def write_params_state(params):
        f = open(STATES_DIR_NAME + 'hotspot.state', 'w')
        f.writelines(json.dumps(params))
        f.close()

    @staticmethod
    def on_exit():
        lg = Logging(LOGS_DIR_NAME + 'main.log')
        lg.write_log('AP', 'Начинаем остановку ТД')
        subprocess.call('pkill dnsmasq', shell=True)
        subprocess.call('pkill hostapd', shell=True)

        if os.path.isfile('/tmp/hostapd.conf'):
            os.remove('/tmp/hostapd.conf')
        if os.path.isfile('/var/lib/misc/dnsmasq.leases'):
            os.remove('/var/lib/misc/dnsmasq.leases')
        if os.path.isfile('/tmp/dhcpd.conf'):
            os.remove('/tmp/dhcpd.conf')
        Firewall.clear_rules()
        params = AccessPoint.read_state()
        params['state'] = 0
        AccessPoint.write_params_state(params)
        lg.write_log('AP', 'ТД остановлена')

# internal_interface = 'wlan1'
# external_interface = 'eth1'
# essid = 'testtesttestAP'
# psk = '123123123'
# channel = 9
#
# ap = AccessPoint()
# ap.set_channel(channel)
# ap.set_essid(essid)
# ap.set_interface(internal_interface)
# ap.set_internet_interface(external_interface)
# ap.set_psk(psk)
# try:
#     ap.start()
#     print('[*] Точка доступа {} запущена.[*]'.format(essid))
#     a = input()
# except Exception as ex:
#     print('[*] Не удалось запустить точку доступа.[*]')
#     print(ex)
#     ap.on_exit()
#     exit(-5)
# ap.on_exit()
# print('[*] Точка доступа {} остановлена.[*]'.format(essid))
