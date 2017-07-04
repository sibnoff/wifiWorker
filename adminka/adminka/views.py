import json
import subprocess
from django.shortcuts import render_to_response
from adminka.source_code.constants import *
from adminka.source_code.mySqlWorker import MySqlWorker
from adminka.source_code.networkAdapters import NetworkAdapters
from adminka.source_code.logging import Logging
from adminka.source_code.clientAndHotspot import Hotspot
from adminka.source_code.accessPoint import AccessPoint
import os


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


def sniff(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Захват пакетов'})


def jammer(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Инъекции в эфир'})


def proxy_server(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Запуск прокси-сервера'})


def rainbow_tables(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Подбор пароля с использованием "радужных таблиц"'})


def download(request):
    return render_to_response('base.html', {'page_name': 'Выгрузка файлов'})


def help_page(request):
    return render_to_response('help.html', {'page_name': 'О программе'})
