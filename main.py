# -*- coding: utf-8 -*-
import time
from accesspoint import AccessPoint
from firewall import Firewall
from constants import *

internal_interface = 'wlan1'
external_interface = 'wlan0'
essid = 'homeAP'
channel = 7
psk = '123123123'

ap = AccessPoint()
ap.set_channel(channel)
ap.set_essid(essid)
ap.set_interface(internal_interface)
ap.set_internet_interface(external_interface)
ap.set_psk(psk)
fw = Firewall()
try:
    ap.start()
    ap.start_dhcp_dns()
    fw.nat(internal_interface, external_interface)
    ap.set_ip_fwd()
    ap.set_route_localnet()
    print('AP started!')
    key_in = True
    while key_in:
        time.sleep(2)

except Exception as ex:
    print(ex)
    print('AP not started!')
ap.on_exit()
fw.on_exit()
print('AP stoped!')
