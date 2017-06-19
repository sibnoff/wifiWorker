from django.shortcuts import render_to_response
from constants import *
from MySqlWorker import MySqlWorker
from NetworkAdapters import NetworkAdapters


def settings(request):
    worker = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
    db_settings = worker.get_settings()
    status = 'БД ДОСТУПНА'
    if not worker.test_connection():
        status = 'БД НЕ ДОСТУПНА'
    db_settings['page_name'] = 'Настройки и диагностика'
    db_settings['connection_status'] = status
    db_settings['iface_list'] = NetworkAdapters.get_all_interfaces()
    db_settings['air_iface_list'] = NetworkAdapters.get_air_interfaces()
    return render_to_response('settings.html', db_settings)


def settings_save(request):
    return render_to_response('settings.html', {'page_name': 'Настройки и диагностика_SAVE'})


def settings_load(request):
    worker = MySqlWorker(CONFIGS_DIR_NAME + 'mySqlConfig.cfg')
    db_settings = worker.get_settings()
    status = 'БД ДОСТУПНА'
    if not worker.test_connection():
        status = 'БД НЕ ДОСТУПНА'
    db_settings['page_name'] = 'Настройки и диагностика_LOAD'
    db_settings['connection_status'] = status
    return render_to_response('settings.html', db_settings)


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
