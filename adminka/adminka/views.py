import json
import subprocess
from django.shortcuts import render_to_response
from adminka.source_code.constants import *
from adminka.source_code.mySqlWorker import MySqlWorker
from adminka.source_code.networkAdapters import NetworkAdapters
from adminka.source_code.logging import Logging
from adminka.source_code.clientAndHotspot import Hotspot
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
    return render_to_response('start_map.html', {'page_name': 'Отображение объектов на карте'})


def show_all_hotspot(request):
    query_all_hotspot = "select bssid, essid, location from `{}`.`hotspots`;".format(DB_NAME)
    worker = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
    result = worker.execute(query_all_hotspot)
    hotspots = []
    if result is not None:
        for row in result:
            hotspots.append(Hotspot(row[0].replace('\n', ''), row[1].replace('\n', ''),
                                    json.loads(row[2])["lat"], json.loads(row[2])["lon"]))
    return render_to_response('update_map.html', {'hotspots': hotspots, 'show_hotspots': 1,
                                                  'show_hotspot': 0, 'show_client': 0})


def hotspot_show(request):
    bssid = request.GET["bssid"]
    essid = request.GET["essid"]
    point = Hotspot(bssid, essid, "", "")
    if bssid != "":
        point.get_info_bssid()
    elif essid != "":
        point.get_info_essid()
    return render_to_response('update_map.html', {'show_hotspots': 0, 'show_hotspot': 1,
                                                  'show_client': 0, 'point': point})


def client_show(request):
    return render_to_response('update_map.html', {'page_name': 'Отображение объектов на карте'})


def download(request):
    return render_to_response('base.html', {'page_name': 'Выгрузка файлов'})


def help_page(request):
    return render_to_response('help.html', {'page_name': 'О программе'})
