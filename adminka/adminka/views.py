import datetime

from django.shortcuts import render_to_response
from django.template import Template, Context
from django.http import HttpResponse
from django.template.loader import get_template


def settings(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Настройки и диагностика',
                                            'work_place': 'ЗДЕСЬ БУДЕТ УПРАВЛЕНИЕ',
                                            'diag_info': 'ТУТ СТАТУСЫ И СООБЩЕНИЯ',
                                            'logs': 'ТУТ БУДУТ ЛОГИ'})


def monitoring(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Мониторинг эфира',
                                            'work_place': 'ЗДЕСЬ БУДЕТ УПРАВЛЕНИЕ',
                                            'diag_info': 'ТУТ СТАТУСЫ И СООБЩЕНИЯ',
                                            'logs': 'ТУТ БУДУТ ЛОГИ'})


def hotspot(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Создание собственной точки доступа',
                                            'work_place': 'ЗДЕСЬ БУДЕТ УПРАВЛЕНИЕ',
                                            'diag_info': 'ТУТ СТАТУСЫ И СООБЩЕНИЯ',
                                            'logs': 'ТУТ БУДУТ ЛОГИ'})


def sniff(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Захват пакетов',
                                            'work_place': 'ЗДЕСЬ БУДЕТ УПРАВЛЕНИЕ',
                                            'diag_info': 'ТУТ СТАТУСЫ И СООБЩЕНИЯ',
                                            'logs': 'ТУТ БУДУТ ЛОГИ'})


def jammer(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Инъекции в эфир',
                                            'work_place': 'ЗДЕСЬ БУДЕТ УПРАВЛЕНИЕ',
                                            'diag_info': 'ТУТ СТАТУСЫ И СООБЩЕНИЯ',
                                            'logs': 'ТУТ БУДУТ ЛОГИ'})


def proxy_server(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Запуск прокси-сервера',
                                            'work_place': 'ЗДЕСЬ БУДЕТ УПРАВЛЕНИЕ',
                                            'diag_info': 'ТУТ СТАТУСЫ И СООБЩЕНИЯ',
                                            'logs': 'ТУТ БУДУТ ЛОГИ'})


def rainbow_tables(request):
    return render_to_response('manage_and_logs.html', {'page_name': 'Подбор пароля с использованием "радужных таблиц"',
                                            'work_place': 'ЗДЕСЬ БУДЕТ УПРАВЛЕНИЕ',
                                            'diag_info': 'ТУТ СТАТУСЫ И СООБЩЕНИЯ',
                                            'logs': 'ТУТ БУДУТ ЛОГИ'})


def map_working(request):
    return render_to_response('map.html', {'page_name': 'Отображение объектов на карте',
                                           'diag_info': 'ТУТ СТАТУСЫ И СООБЩЕНИЯ'})


def download(request):
    return render_to_response('base.html', {'page_name': 'Выгрузка файлов',
                                            'work_place': 'ЗДЕСЬ БУДЕТ УПРАВЛЕНИЕ',
                                            'diag_info': 'ТУТ СТАТУСЫ И СООБЩЕНИЯ',
                                            'logs': 'ТУТ БУДУТ ЛОГИ'})


def help_page(request):
    return render_to_response('help.html', {'page_name': 'О программе',
                                            'diag_info': 'ТУТ СТАТУСЫ И СООБЩЕНИЯ'})
