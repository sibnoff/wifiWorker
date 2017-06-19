# -*- coding: utf-8 -*-
from Complete.Firewall import Firewall
from Complete.accesspoint import AccessPoint
from actions import Actions
from menu import Menu

internal_interface = 'wlan2'
external_interface = 'wlan0'
essid = 'homeAP'
channel = 6
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
    print('[{}*{}] Точка доступа {} запущена.[{}*{}]'.format(G, W, essid, G, W))
    ap.start_dhcp_dns()
    print('[{}*{}] DHCP/DNS сервер запущен.[{}*{}]'.format(G, W, G, W))
    fw.nat(internal_interface, external_interface)
    ap.set_ip_fwd()
    ap.set_route_localnet()
    print('[{}*{}] Параметры маршрутизации заданы.[{}*{}]'.format(G, W, G, W))
except Exception as ex:
    print('[{}*{}] Не удалось запустить точку доступа.[{}*{}]'.format(R, W, R, W))
    print(ex)
    ap.on_exit()
    fw.on_exit()
    exit(-5)
key_in = True
menu = Menu()
menu.set_items([1, 2, 0])
act = Actions()
clients = dict()
rules = dict()
while key_in:
    menu.show()
    item = menu.get_choose(input())
    if item == 0:
        key_in = False
    act.run(item, ap, clients, rules)
