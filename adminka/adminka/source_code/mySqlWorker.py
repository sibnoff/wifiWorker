import json
import os
import pymysql
from pymysql import Error
from adminka.source_code.constants import *
from adminka.source_code.logging import Logging


class MySqlWorker:
    def __init__(self, file_name, set_config=False):
        if set_config:
            self._settings = dict()
            self.log = Logging(LOGS_DIR_NAME + 'main.log')
            self._file_cfg = file_name
            return
        self.log = Logging(LOGS_DIR_NAME + 'main.log')
        if not os.path.isfile(file_name):
            raise FileNotFoundError('Не найден конфигурационный '
                                    'файл: {}'.format(file_name))
        self._file_cfg = file_name
        self._settings = dict()
        self._con = None
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
        self.log.write_log("MYSQL", "SAVE_SETTINGS")
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
            self.log.write_log("MYSQL", "CON_SUCCESSFUL")
            return True
        except Exception as ex:
            self.log.write_log("MYSQL_ER", ex)
            return False

    def open_connection(self):
        try:
            if self._con is None:
                self._con = pymysql.connect(host=self._settings['db_host'],
                                            user=self._settings['db_user'],
                                            passwd=self._settings['db_password'],
                                            use_unicode=True, charset="utf8")
            else:
                self._con.ping()
            return 1
        except Error as e:
            self.log.write_log("MYSQL_ER", str(e))
            return None

    def close_connection(self):
        try:
            if self._con is not None:
                self._con.close()
            return 1
        except Error as e:
            self.log.write_log("MYSQL_ER", str(e))
            return None

    # метод выполняет запрос, результат которого - скаляр
    def execute_scalar(self, query):
        self.open_connection()
        try:
            cur = self._con.cursor()
            cur.execute(query)
            res = cur.fetchone()
            self.log.write_log("MYSQL", "EXECUTE_OK")
            return res
        except Exception as ex:
            self.log.write_log("MYSQL_ER", ex)
            return None
        finally:
            self.close_connection()

    # метод выполняет запрос, результат которого - множество
    def execute(self, query):
        self.open_connection()
        try:
            cur = self._con.cursor()
            cur.execute(query)
            res = cur.fetchall()
            self.log.write_log("MYSQL", "EXECUTE_OK")
            return res
        except Exception as ex:
            self.log.write_log("MYSQL_ER", ex)
            return None
        finally:
            self.close_connection()

    # метод выполняет запрос без результата (insert, update)
    def execute_none(self, query):
        self.open_connection()
        try:
            cur = self._con.cursor()
            cur.execute(query)
            self._con.commit()
            self.log.write_log("MYSQL", "INSERT(UPDATE)_OK")
            return True
        except Exception as ex:
            self.log.write_log("MYSQL_ER", ex)
            return None
        finally:
            self.close_connection()

# mysql = MySqlWorker()
# print(mysql.get_settings())
