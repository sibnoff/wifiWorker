import datetime
import json
from adminka.source_code.constants import *
from adminka.source_code.logging import Logging
from adminka.source_code.mySqlWorker import MySqlWorker


class Client:
    """Клиент точки доступа. Атрибуты:
        - MAC
        - curent_ip
        - nick
        - ESSID текущей ТД"""

    def __init__(self, mac, cur_ip, nick, essid):
        self.mac = mac
        self.cur_ip = cur_ip
        if nick is None:
            self.nick = mac
        else:
            self.nick = nick
        self._essid = essid
        self._log = Logging(LOGS_DIR_NAME + 'main.log')

    def __str__(self):
        """Возвращает строку: MAC:current_ip:nick"""
        return 'mac:{}, ip:{}, nick:{}'.format(self.mac, self.cur_ip, self.nick)

    # назначаем ник клиенту
    def set_nick(self, nick):
        self.nick = nick

    # вставляем (обновляем) информацию о клиенте в БД
    def insert_info(self):
        mw = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
        query_insert = "insert into {}.clients (dateInsert, mac, " \
                       "nick, lastEssid, dateUpdate) values " \
                       "('{}', '{}', '{}', '{}', '{}')" \
                       "on duplicate key update lastEssid = '{}', " \
                       "dateUpdate = '{}'".format(DB_NAME, datetime.datetime.now(),
                                                  self.mac, self.nick, self._essid,
                                                  datetime.datetime.now(), self._essid,
                                                  datetime.datetime.now())
        if mw.execute_none(query_insert) is None:
            self._log.write_log("INSERT_ERROR", "Не удалось выполнить вставку клиента.")

    # вставляем информацию о местоположении клиента
    @staticmethod
    def insert_geolocation(mac, location):
        mw = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
        query_insert = "insert into {}.geolocations (dateInsert, clients_mac, location) values " \
                       "('{}', '{}', '{}');".format(DB_NAME, datetime.datetime.now(),
                                                    mac, location)
        if mw.execute_none(query_insert) is None:
            lg = Logging(LOGS_DIR_NAME + 'main.log')
            lg.write_log("INSERT_ERROR", "Не удалось выполнить вставку местоположения.")
            return False
        return True

    # получаем самый свежий мак адрес по ip адресу
    @staticmethod
    def get_mac_for_ip(ip):
        mw = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
        query_mac = 'select clients_mac from {}.addresses where ' \
                    'clients_ip = {} order by dateInsert desc limit 1'.format(DB_NAME, ip)
        tmp = mw.execute_scalar(query_mac)
        if tmp is None:
            lg = Logging(LOGS_DIR_NAME + 'main.log')
            lg.write_log("SELECT_ERROR", "Не удалось выполнить запрос ника клиента.")
            return None
        return tmp[0]

    # вставляем информацию о подключении клиента к ТД
    @staticmethod
    def insert_connection(mac, bssid, essid):
        mw = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
        query_insert = "insert into {}.connections (dateInsert, clients_mac, bssid, essid) values " \
                       "('{}', '{}', '{}', '{}');".format(DB_NAME, datetime.datetime.now(),
                                                          mac, bssid, essid)
        if mw.execute_none(query_insert) is None:
            lg = Logging(LOGS_DIR_NAME + 'main.log')
            lg.write_log("INSERT_ERROR", "Не удалось выполнить вставку информации о подключении к ТД.")
            return False
        return True

    # получаем ник для mac адреса из БД
    @staticmethod
    def get_nick(mac):
        mw = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
        query_nick = 'select nick from {}.clients where mac = {} limit 1'.format(DB_NAME, mac)
        tmp = mw.execute_scalar(query_nick)
        if tmp is None:
            lg = Logging(LOGS_DIR_NAME + 'main.log')
            lg.write_log("SELECT_ERROR", "Не удалось выполнить запрос ника клиента.")
            return None
        return tmp[0]

    # обновляем ник клиента в БД
    def update_nick_in_db(self):
        mw = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
        query_update = "update {}.clients set nick = '{}' " \
                       "where mac = '{}'".format(DB_NAME, self.nick,
                                                 self.mac)
        if mw.execute_none(query_update) is None:
            self._log.write_log("UPDATE_ERROR", "Не удалось выполнить обновление ника клиента.")

    # обновляем юзерагента клиента по маку
    @staticmethod
    def update_user_agent(user_agent, mac):
        mw = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
        query_update = "update {}.clients set userAgent = '{}' " \
                       "where mac = '{}'".format(DB_NAME, user_agent, mac)
        if mw.execute_none(query_update) is None:
            lg = Logging(LOGS_DIR_NAME + 'main.log')
            lg.write_log("UPDATE_ERROR", "Не удалось выполнить обновление информации о UserAgent клиента.")
            return False

    # получаем всю информацию о клиенте из таблицы clients
    def get_info(self):
        mw = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
        query_info = 'select * from {}.clients where mac = {} limit 1'.format(DB_NAME, self.mac)
        tmp = mw.execute_scalar(query_info)
        if tmp is None:
            self._log.write_log("SELECT_ERROR", "Не удалось выполнить запрос информации о клиенте.")
            return None
        return tmp


class Hotspot:
    def __init__(self, bssid, essid, latitude, longitude):
        self.bssid = bssid
        self.essid = essid
        self.lat = latitude
        self.lon = longitude
        self._log = Logging(LOGS_DIR_NAME + 'main.log')

    # метод преобразует координаты в json
    @staticmethod
    def loc_to_json(lat, lon):
        data = {"lat": lat, "lon": lon}
        return json.dumps(data)

    # задаем координаты ТД
    def set_location(self, latitude, longitude):
        self.lat = latitude
        self.lon = longitude

    # вставляем инфу о ТД в БД
    def insert_info(self):
        mw = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
        query_clone = "select count(*) from {}.hotspots where essid = '{}' " \
                      "and bssid = '{}'".format(DB_NAME, self.essid,
                                                self.bssid)
        tmp = mw.execute_scalar(query_clone)
        if tmp is None:
            self._log.write_log('SELECT_ERROR', 'Не удалось поискать информацию о ТД.')
            return
        if int(tmp[0]) != 0:
            query_update = "update {}.hotspots set " \
                           "location = '{}', dateUpdate = " \
                           "'{}'".format(DB_NAME, self.loc_to_json(),
                                         datetime.datetime.now())
            if mw.execute_none(query_update) is None:
                self._log.write_log("UPDATE_ERROR", "Не удалось выполнить "
                                                    "обновление информации о ТД.")
            return
        query_insert = "insert into {}.hotspots (dateInsert, essid, " \
                       "bssid, location, dateUpdate) values ('{}', '{}', " \
                       "'{}', '{}', '{}')".format(DB_NAME, datetime.datetime.now(),
                                                  self.essid, self.bssid,
                                                  Hotspot.loc_to_json(self.lat, self.lon),
                                                  datetime.datetime.now())
        if mw.execute_none(query_insert) is None:
            self._log.write_log("INSERT_ERROR", "Не удалось выполнить вставку ТД.")

    # получаем инфу о ТД из БД
    def get_info_bssid(self):
        mw = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
        query_info = "select essid, location from {}.hotspots where " \
                     "bssid = '{}' limit 1".format(DB_NAME, self.bssid)
        result = mw.execute(query_info)
        if result is None:
            self._log.write_log("SELECT_ERROR", "Не удалось выполнить запрос информации о ТД.")
            return None
        if len(result) == 0:
            self._log.write_log("NOT_FOUND", "Не удалось найти информацию о ТД.")
            return None
        self.essid = result[0][0]
        self.lat = json.loads(result[0][1])['lat']
        self.lon = json.loads(result[0][1])['lon']
        self._log.write_log("FOUND", "Информация о ТД найдена.")
        return True

    def get_info_essid(self):
        mw = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
        query_info = "select bssid, location from {}.hotspots where " \
                     "essid = '{}' limit 1".format(DB_NAME, self.essid)
        result = mw.execute(query_info)
        if result is None:
            self._log.write_log("SELECT_ERROR", "Не удалось выполнить запрос информации о ТД.")
            return None
        if len(result) == 0:
            self._log.write_log("NOT_FOUND", "Не удалось найти информацию о ТД.")
            return None
        self.bssid = result[0][0]
        self.lat = json.loads(result[0][1])['lat']
        self.lon = json.loads(result[0][1])['lon']
        self._log.write_log("FOUND", "Информация о ТД найдена.")
        return True

# cl = Client("123", '192.168.1.1', 'вапрв', 'чапртвп')
# cl.insert_info()
# print(Client.get_nick('123'))
# cl.set_nick('AAA')
# cl.update_nick_in_db()
# print(cl.get_info())
#
# td = Hotspot('kdjhf', '111', '56', '65')
# print(td.loc_to_json())
# td.insert_info()
# print(td.get_info())

# essids = open('Complete/essids_izmailovo', 'r').readlines()
# bssids = open('Complete/bssids_izmailovo', 'r').readlines()
#
# for i in range(len(essids)):
#     td = Hotspot(bssids[i], essids[i], '55.791878', '37.74847')
#     td.insert_info()
#
# essids = open('Complete/essids_akados', 'r').readlines()
# bssids = open('Complete/bssids_akados', 'r').readlines()
#
# for i in range(len(essids)):
#     td = Hotspot(bssids[i], essids[i], '55.684267', '37.471305')
#     td.insert_info()
#
# essids = open('Complete/essids_selhoz13', 'r').readlines()
# bssids = open('Complete/bssids_selhoz13', 'r').readlines()
#
# for i in range(len(essids)):
#     td = Hotspot(bssids[i], essids[i], '55.836449', '37.639242')
#     td.insert_info()

# essids = open('Complete/essids_yasnogor', 'r').readlines()
# bssids = open('Complete/bssids_yasnogor', 'r').readlines()
#
# for i in range(len(essids)):
#     td = Hotspot(bssids[i], essids[i], '55.601738', '37.533458')
#     td.insert_info()
