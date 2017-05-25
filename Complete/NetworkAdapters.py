import netifaces
import re
import subprocess

import time

ER = open('log_error.txt', 'w')


class NetworkAdapters:
    @staticmethod
    def get_all_interfaces():
        """метод возвращает список всех доступных
        сетевых интерфесов системы"""
        return netifaces.interfaces()

    @staticmethod
    def get_air_interfaces():
        """метод возвращает список всех беспроводных
        интерфейсов системы"""
        air_interfaces = []
        for iface in netifaces.interfaces():
            p = subprocess.Popen(["iwconfig", iface],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=ER)
            out, err = p.communicate()
            if out.decode('utf-8') != '':
                air_interfaces.append(iface)
        return air_interfaces

    @staticmethod
    def down_iface(iface):
        """Метод тушит сетевой интерфейс"""
        if iface not in NetworkAdapters.get_all_interfaces():
            raise ValueError('{} не является интерфейсом'.format(iface))
        p = subprocess.Popen(["sudo", "ifconfig", iface, "down"],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=ER)
        out, err = p.communicate()

    @staticmethod
    def up_iface(iface):
        """Метод поднимает сетевой интерфейс"""
        if iface not in NetworkAdapters.get_all_interfaces():
            raise ValueError('{} не является интерфейсом'.format(iface))
        p = subprocess.Popen(["sudo", "ifconfig", iface, "up"],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=ER)
        out, err = p.communicate()

    @staticmethod
    def get_active_interfaces():
        """Метод возвращает активные
        сетевые интерфейсы"""
        active_iface = []
        p = subprocess.Popen(["ifconfig"],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=ER)
        out, err = p.communicate()
        for iface in netifaces.interfaces():
            if iface in out.decode(encoding='utf-8'):
                active_iface.append(iface)
        return active_iface

    @staticmethod
    def is_active(iface):
        """Метод проверяет, является ли активным интерефейс"""
        if iface not in NetworkAdapters.get_all_interfaces():
            raise ValueError('{} не является интерфейсом'.format(iface))
        if iface in NetworkAdapters.get_active_interfaces():
            return True
        else:
            return False

    @staticmethod
    def set_mode(iface, mode):
        """Метод задает режим работы для беспроводного
        интерфейса(тушит, задает режим, поднимает)"""
        if iface not in NetworkAdapters.get_air_interfaces():
            raise ValueError('{} не является беспроводным '
                             'адаптером'.format(iface))
        if mode not in ['managed', 'monitor', 'master']:
            raise ValueError('Не коректно задан режим работы '
                             'адаптера: {}'.format(mode))
        subprocess.call("ifconfig {} down && "
                        "iwconfig {} mode {} && "
                        "ifconfig {} "
                        "up".format(iface, iface,
                                    mode, iface), shell=True)
        time.sleep(1)

    @staticmethod
    def get_info(iface):
        """Метод возвращает текущую статистику ативного сетевого
        интерфейса в виде строки(как есть с консоли)"""
        if iface not in NetworkAdapters.get_active_interfaces():
            raise ValueError('Интерфейс {} не является '
                             'активным.'.format(iface))
        if iface in NetworkAdapters.get_air_interfaces():
            p = subprocess.Popen(["iwconfig", iface],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=ER)
            out, err = p.communicate()
        else:
            p = subprocess.Popen(["ifconfig", iface],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=ER)
            out, err = p.communicate()
        return out.decode(encoding='utf-8')

    @staticmethod
    def get_mode(iface):
        """Метод возвращает текущий режим работы
        активного беспроводного интерфейса"""
        if iface not in NetworkAdapters.get_active_interfaces():
            raise ValueError('Интерфейс {} не является '
                             'активным.'.format(iface))
        if iface not in NetworkAdapters.get_air_interfaces():
            raise ValueError('{} не является беспроводным '
                             'адаптером'.format(iface))
        p = subprocess.Popen(["iwconfig", iface],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=ER)
        out, err = p.communicate()
        mode = r"Mode:(?P<mode>[a-zA-Z]+)\s+"
        matches = re.search(mode, out.decode(encoding='utf-8'))
        return matches.groupdict()['mode']


interface = 'wlan2'

# выводим все сетевые интерфейсы
print(NetworkAdapters.get_all_interfaces())

# выводим все беспроводные интерфейсы
print(NetworkAdapters.get_air_interfaces())

# выводим все ативные сетевые интерфейсы
print(NetworkAdapters.get_active_interfaces())

# тушим интерфейс
NetworkAdapters.down_iface(interface)

# выводим все ативные сетевые интерфейсы
print(NetworkAdapters.get_active_interfaces())

# поднимаем интерфейс
NetworkAdapters.up_iface(interface)
print(NetworkAdapters.get_mode(interface))

# меняем режим работы интерфеса
NetworkAdapters.set_mode(interface, 'monitor')

# вывод режима работы интерфейса
print(NetworkAdapters.get_mode(interface))

# вывод режима работы интерфейса
NetworkAdapters.set_mode(interface, 'managed')

# вывод статистики по интерфейсу
print(NetworkAdapters.get_info(interface))
