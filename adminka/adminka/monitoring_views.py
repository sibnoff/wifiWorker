from django.shortcuts import render_to_response
from adminka.source_code.constants import *
from adminka.source_code.networkAdapters import NetworkAdapters
from adminka.source_code.logging import Logging


def monitoring(request):
    mon_settings = dict()
    mon_settings['page_name'] = 'Мониторинг эфира'
    mon_settings['air_iface_list'] = NetworkAdapters.get_air_interfaces()
    return render_to_response('monitoring.html', mon_settings)


def start_monitoring(request):
    lg = Logging(LOGS_DIR_NAME + 'main.log')
    mon_iface = request.POST['mon_iface']
    lg.write_log('Monitoring', 'mon_iface: {}'.format(mon_iface))
    if mon_iface == 'undefined':
        lg.write_log('Monitoring', 'Интерфейс не выбран')
        return render_to_response('monitor_mode.html', {'mon_status': 0})
    return render_to_response('monitor_mode.html', {'mon_status': 1})


def stop_monitoring(request):
    return render_to_response('monitor_mode.html', {'mon_status': 0})


def monitoring_get_logs(request):
    return render_to_response("monitor_logs.html", {'clients': {}, 'hotspots': {}})
