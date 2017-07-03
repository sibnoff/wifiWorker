from django.shortcuts import render_to_response
from adminka.source_code.constants import *
from adminka.source_code.mySqlWorker import MySqlWorker
from adminka.source_code.networkAdapters import NetworkAdapters


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


def iface_change_state(request):
    raise NotImplementedError


def air_iface_change_mode(request):
    raise NotImplementedError
