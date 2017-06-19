#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json

from Logging import Logging
from MySqlWorker import MySqlWorker
from constants import *


class Client:
    """Клиент точки доступа. Атрибуты:
        - MAC
        - curent_ip
        - nick
        - ESSID текущей ТД"""

    def __init__(self, mac, cur_ip, nick, essid):
        self._mac = mac
        self._cur_ip = cur_ip
        if nick is None:
            self._nick = mac
        else:
            self._nick = nick
        self._essid = essid
        self._log = Logging(LOGS_DIR_NAME + 'main.log')

    def __str__(self):
        """Возвращает строку: MAC:current_ip:nick"""
        return 'mac:{}, ip:{}, nick:{}'.format(self._mac, self._cur_ip, self._nick)

    # назначаем ник клиенту
    def set_nick(self, nick):
        self._nick = nick

    # вставляем (обновляем) информацию о клиенте в БД
    def insert_info(self):
        mw = MySqlWorker()
        query_insert = "insert into {}.clients (dateInsert, mac, " \
                       "nick, lastEssid, dateUpdate) values " \
                       "('{}', '{}', '{}', '{}', '{}')" \
                       "on duplicate key update lastEssid = '{}', " \
                       "dateUpdate = '{}'".format(DB_NAME, datetime.datetime.now(),
                                                  self._mac, self._nick, self._essid,
                                                  datetime.datetime.now(), self._essid,
                                                  datetime.datetime.now())
        if mw.execute_none(query_insert) is None:
            self._log.write_log("INSERT_ERROR", "Не удалось выполнить вставку клиента.")

    # получаем ник для mac адреса из БД
    @staticmethod
    def get_nick(mac):
        mw = MySqlWorker()
        query_nick = 'select nick from {}.clients where mac = {} limit 1'.format(DB_NAME, mac)
        tmp = mw.execute_scalar(query_nick)
        if tmp is None:
            lg = Logging('Complete/logs/main.log')
            lg.write_log("SELECT_ERROR", "Не удалось выполнить запрос ника клиента.")
            return None
        return tmp[0]

    # обновляем ник клиента в БД
    def update_nick_in_db(self):
        mw = MySqlWorker()
        query_update = "update {}.clients set nick = '{}' " \
                       "where mac = '{}'".format(DB_NAME, self._nick,
                                                 self._mac)
        if mw.execute_none(query_update) is None:
            self._log.write_log("UPDATE_ERROR", "Не удалось выполнить обновление ника клиента.")

    # получаем всю информацию о клиенте из таблицы clients
    def get_info(self):
        mw = MySqlWorker()
        query_info = 'select * from {}.clients where mac = {} limit 1'.format(DB_NAME, self._mac)
        tmp = mw.execute_scalar(query_info)
        if tmp is None:
            self._log.write_log("SELECT_ERROR", "Не удалось выполнить запрос информации о клиенте.")
            return None
        return tmp


class Hotspot:
    def __init__(self, bssid, essid, latitude, longitude):
        self._bssid = bssid
        self._essid = essid
        self._loc_lat = latitude
        self._loc_lon = longitude
        self._log = Logging('Complete/logs/main.log')

    # метод преобразует координаты в json
    def loc_to_json(self):
        data = {"lat": self._loc_lat, "lon": self._loc_lon}
        return json.dumps(data)

    # задаем координаты ТД
    def set_location(self, latitude, longitude):
        self._loc_lat = latitude
        self._loc_lon = longitude

    # вставляем инфу о ТД в БД
    def insert_info(self):
        mw = MySqlWorker()
        query_clone = "select count(*) from {}.hotspots where essid = '{}' " \
                      "and bssid = '{}'".format(DB_NAME, self._essid,
                                                self._bssid)
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
                                                  self._essid, self._bssid,
                                                  self.loc_to_json(),
                                                  datetime.datetime.now())
        if mw.execute_none(query_insert) is None:
            self._log.write_log("INSERT_ERROR", "Не удалось выполнить вставку ТД.")

    # получаем инфу о ТД из БД
    def get_info(self):
        mw = MySqlWorker()
        query_info = "select * from {}.hotspots where " \
                     "essid = '{}' and bssid = '{}' " \
                     "limit 1".format(DB_NAME, self._essid,
                                      self._bssid)
        tmp = mw.execute_scalar(query_info)
        if tmp is None:
            self._log.write_log("SELECT_ERROR", "Не удалось выполнить запрос информации о ТД.")
            return None
        return tmp


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

essids = open('Complete/essids_yasnogor', 'r').readlines()
bssids = open('Complete/bssids_yasnogor', 'r').readlines()

for i in range(len(essids)):
    td = Hotspot(bssids[i], essids[i], '55.601738', '37.533458')
    td.insert_info()
