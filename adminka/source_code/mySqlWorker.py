import json
import os
import pymysql
from constants import *
from Logging import Logging


class MySqlWorker:
    def __init__(self, file_name, set_config=False):
        if set_config:
            self._settings = dict()
            self.log = Logging(LOGS_DIR_NAME + 'mySqlWorker.log')
            self._file_cfg = file_name
            return
        self.log = Logging(LOGS_DIR_NAME + 'mySqlWorker.log')
        if not os.path.isfile(file_name):
            raise FileNotFoundError('Не найден конфигурационный '
                                    'файл: {}'.format(file_name))
        self._file_cfg = file_name
        self._settings = dict()
        if not self.read_config():
            raise ValueError('Некорректное содержимое конфигурационного файла.')
        self.test_connection()

    # метод для чтения конфига БД
    def read_config(self):
        f = open(self._file_cfg, 'r')
        text = f.readline()
        f.close()
        try:
            json_data = json.loads(text)
        except Exception as ex:
            self.log.write_log("JSON", ex)
            return False
        self._settings = json_data
        return True

    def set_config(self, host, name, login, passwd):
        self._settings['db_host'] = host
        self._settings['db_name'] = name
        self._settings['db_user'] = login
        self._settings['db_password'] = passwd

    def write_config(self):
        f = open(self._file_cfg, 'w')
        try:
            f.writelines(json.dumps(self._settings))
        except Exception as ex:
            self.log.write_log("JSON", ex)
            return False
        f.close()
        return True

    # метод возвращает настройки в виде словаря
    def get_settings(self):
        return self._settings

    # метод проверяет доступность БД
    def test_connection(self):
        try:
            con = pymysql.connect(host=self._settings['db_host'],
                                  user=self._settings['db_user'],
                                  passwd=self._settings['db_password'])
            con.close()
            self.log.write_log("CONNECT", "CONNECTION SUCCESSFUL")
            return True
        except Exception as ex:
            self.log.write_log("CON_ERROR", ex)
            return False

    # метод выполняет запрос, результат которого - скаляр
    def execute_scalar(self, query):
        try:
            con = pymysql.connect(host=self._settings['db_host'],
                                  user=self._settings['db_user'],
                                  passwd=self._settings['db_password'],
                                  use_unicode=True, charset="utf8")
            self.log.write_log("CONNECT", "CONNECTION SUCCESSFUL")
        except Exception as ex:
            self.log.write_log("CON_ERROR", ex)
            return None
        try:
            cur = con.cursor()
            cur.execute(query)
            res = cur.fetchone()
            con.close()
            self.log.write_log("EXECUTE", "OK")
            return res
        except Exception as ex:
            self.log.write_log("EXE_ERROR", ex)
            return None

    # метод выполняет запрос, результат которого - множество
    def execute(self, query):
        try:
            con = pymysql.connect(host=self._settings['db_host'],
                                  user=self._settings['db_user'],
                                  passwd=self._settings['db_password'],
                                  use_unicode=True, charset="utf8")
            self.log.write_log("CONNECT", "CONNECTION SUCCESSFUL")
        except Exception as ex:
            self.log.write_log("CON_ERROR", ex)
            return None
        try:
            cur = con.cursor()
            cur.execute(query)
            res = cur.fetchall()
            con.close()
            self.log.write_log("EXECUTE", "OK")
            return res
        except Exception as ex:
            self.log.write_log("EXE_ERROR", ex)
            return None

    # метод выполняет запрос без результата (insert, update)
    def execute_none(self, query):
        try:
            con = pymysql.connect(host=self._settings['db_host'],
                                  user=self._settings['db_user'],
                                  passwd=self._settings['db_password'],
                                  use_unicode=True, charset="utf8")
            self.log.write_log("CONNECT", "CONNECTION SUCCESSFUL")
        except Exception as ex:
            self.log.write_log("CON_ERROR", ex)
            return None
        try:
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            con.close()
            self.log.write_log("EXECUTE", "OK")
            return True
        except Exception as ex:
            self.log.write_log("EXE_ERROR", ex)
            return None

# mysql = MySqlWorker()
# print(mysql.get_settings())

