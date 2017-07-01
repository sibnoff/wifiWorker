import subprocess

from django.shortcuts import render_to_response
from adminka.source_code.constants import *
from adminka.source_code.mySqlWorker import MySqlWorker
from adminka.source_code.networkAdapters import NetworkAdapters
from adminka.source_code.logging import Logging
import os


def settings(request):
    worker = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
    db_settings = worker.get_settings()
    status = '1'
    if not worker.test_connection():
        status = 0
    db_settings['page_name'] = 'Настройки и диагностика'
    db_settings['connection_status'] = status
    db_settings['iface_list'] = NetworkAdapters.get_all_interfaces()
    db_settings['air_iface_list'] = NetworkAdapters.get_air_interfaces()
    return render_to_response('settings.html', db_settings)


def settings_save(request):
    worker = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg', set_config=True)
    worker.set_config(request.POST['db_host'],
                      request.POST['db_name'],
                      request.POST['db_user'],
                      request.POST['db_password'])
    worker.write_config()

    db_settings = worker.get_settings()
    status = '1'
    if not worker.test_connection():
        status = 0
    db_settings['page_name'] = 'Настройки и диагностика'
    db_settings['connection_status'] = status
    return render_to_response('load_settings.html', db_settings)


def settings_load(request):
    worker = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
    db_settings = worker.get_settings()
    status = '1'
    if not worker.test_connection():
        status = 0
    db_settings['connection_status'] = status
    return render_to_response('load_settings.html', db_settings)


def get_tail_log(request):
    try:
        count = int(request.GET['count_rows'])
        name = request.GET['file_name']
    except Exception as ex:
        return render_to_response("get_logs.html", {'log_rows': []})
    f = open(LOGS_DIR_NAME + name, 'r')
    rows = f.readlines()
    f.close()
    if len(rows) < count:
        return render_to_response("get_logs.html", {'log_rows': sorted(rows, reverse=True)})
    else:
        return render_to_response("get_logs.html", {'log_rows': sorted(rows[len(rows) - count:], reverse=True)})


def iface_change_state(request):
    raise NotImplementedError


def air_iface_change_mode(request):
    raise NotImplementedError


def monitoring(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Мониторинг эфира'})


def hotspot(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Создание собственной точки доступа'})


def sniff(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Захват пакетов'})


def jammer(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Инъекции в эфир'})


def proxy_server(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Запуск прокси-сервера'})


def rainbow_tables(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Подбор пароля с использованием "радужных таблиц"'})


def map_working(request):
    return render_to_response('map.html', {'page_name': 'Отображение объектов на карте'})


def download(request):
    return render_to_response('base.html', {'page_name': 'Выгрузка файлов'})


def help_page(request):
    return render_to_response('help.html', {'page_name': 'О программе'})
