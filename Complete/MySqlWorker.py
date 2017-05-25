import json
import os
import pymysql
from Complete.Logging import Logging


class MySqlWorker:
    def __init__(self):
        self.log = Logging('Complete/logs/mySqlWorker.log')
        file_name_cfg = 'Complete/mySqlConfig.cfg'
        if not os.path.isfile(file_name_cfg):
            raise FileNotFoundError('Не найден конфигурационный '
                                    'файл: {}'.format(file_name_cfg))
        self._file_cfg = file_name_cfg
        self._settings = dict()
        if not self.read_config(file_name_cfg):
            raise ValueError('Некорректное содержимое конфигурационного файла.')
        self.test_connection()

    # метод для чтения конфига БД
    def read_config(self, file_name):
        f = open(file_name, 'r')
        text = f.readline()
        f.close()
        try:
            json_data = json.loads(text)
        except Exception as ex:
            self.log.write_log("JSON", ex)
            return False
        self._settings = json_data
        return True

    # метод возвращает текущие натсройки БД в формате json
    def show_settings(self):
        print(self._settings)

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
# mysql.show_settings()
