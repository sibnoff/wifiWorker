from subprocess import Popen, PIPE

from accesspoint import AccessPoint
from firewall import Firewall
from constants import *
from clientStation import ClientStation
from menu import Menu


class Actions:
    def run(self, item, ap, clients, rules):
        if item == 0:
            self.shut_down_ap()
        if item == 1:
            self.show_clients(ap, clients)
        if item == 2:
            self.show_redirect_rules(rules)
        if item == 3:
            self.add_redirect_rules(rules)
        if item == 4:
            self.del_redirect_rules(rules)
        if item == 5:
            self.clear_redirect_rules(rules)

    @staticmethod
    def shut_down_ap():
        print('[{}*{}] Останавливаю точку доступа и dhcp сервер...[{}*{}]'.format(G, W, G, W))
        AccessPoint.on_exit()
        print('[{}*{}] Очищаю iptables...[{}*{}]'.format(G, W, G, W))
        Firewall.clear_rules()
        print('[{}*{}] Работа завершена.[{}*{}]'.format(G, W, G, W))
        return

    @staticmethod
    def show_clients(ap, clients):
        clients.clear()
        try:
            iw = Popen('iw dev {} station dump'.format(ap.interface), shell=True, stdout=PIPE, stdin=PIPE)
            iw = iw.stdout.read().decode().split('\n')
            for line in iw:
                if 'Station' in line:
                    mac = line.split()[1]
                if 'signal:' in line:
                    signal = line.split(':')[1].replace(' ', '').replace('\t', '')
                    clients[mac] = ClientStation(mac)
                    clients[mac].add_trasted_essid(ap.essid)
                    clients[mac].set_signal(signal)
                    arp = Popen('arp', shell=True, stdout=PIPE, stdin=PIPE)
                    arp = arp.stdout.read().decode().split('\n')
                    for station in arp:
                        if mac in station:
                            ip = station.split()[0]
                            clients[mac].set_ip(ip)

        except Exception as exc:
            print('[-] iw is failed!\n{}\n'.format(exc))
            return
        if len(clients) == 0:
            print('\tКлиенты отсутствуют')
            return
        i = 1
        for client in clients:
            print('{}. {}'.format(i, clients[client].get_full_info()))
            i += 1

    def show_redirect_rules(self, rules):
        if len(rules) != 0:
            i = 1
            print('Текущие сайты для редиректа:')
            for name in rules.keys():
                print('{}. {}'.format(i, name))
                i += 1
        else:
            print('Список для редиректа пуст.')
        list_files = os.listdir('sites_address')
        avaib_sites = dict()
        if len(list_files) == 0:
            print('Отсутствуют конфигурационные файлы для сайтов')
        else:
            print('Доступные сайты для редиректа:')
            i = 1
            for file in list_files:
                list_ip = open('sites_address/{}'.format(file), 'r').readlines()
                avaib_sites[file] = list_ip
                print('{}. {} -->> {}'.format(i, file, avaib_sites[file]))
                i += 1
        menu = Menu()
        menu.set_items([3, 4, 5, 6])
        menu.show()
        item = menu.get_choose(input())
        if item == 6:
            return
        self.run(item, None, None, rules)

    def add_redirect_rules(self, rules):
        list_files = os.listdir('sites_address')
        avaib_sites = dict()
        if len(list_files) == 0:
            print('Отсутствуют конфигурационные файлы для сайтов')
        else:
            print('Доступные сайты для редиректа:')
            i = 1
            for file in list_files:
                list_ip = open('sites_address/{}'.format(file), 'r').readlines()
                avaib_sites[file] = list_ip
                print('{}. {} -->> {}'.format(i, file, avaib_sites[file]))
                i += 1

    def del_redirect_rules(self, rules):
        raise NotImplementedError

    @staticmethod
    def clear_redirect_rules(rules):
        rules.clear()
        raise NotImplementedError
