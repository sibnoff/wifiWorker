import subprocess
from django.shortcuts import render_to_response
from adminka.source_code.constants import *
from adminka.source_code.networkAdapters import NetworkAdapters
from adminka.source_code.logging import Logging
from adminka.source_code.accessPoint import AccessPoint
from adminka.source_code.clientAndHotspot import Client


def hotspot(request):
    hs_settings = dict()
    hs_settings['page_name'] = 'Создание собственной точки доступа'
    hs_settings['iface_list'] = NetworkAdapters.get_all_interfaces()
    hs_settings['air_iface_list'] = NetworkAdapters.get_air_interfaces()
    state = AccessPoint.read_state()
    hs_settings['ap_status'] = state['state']
    return render_to_response('hotspot.html', hs_settings)


def hotspot_get_logs(request):
    f = open(LOGS_DIR_NAME + 'hostapd.output', 'r')
    rows = f.readlines()
    f.close()
    clients_connected = []
    con_string = 'AP-STA-CONNECTED'
    discon_string = 'AP-STA-DISCONNECTED'
    for row in rows:
        start_index = row.find(con_string)
        if start_index != -1:
            mac = row[start_index + 1 + len(con_string):].lstrip().rstrip()
            if mac not in clients_connected:
                clients_connected.append(mac)
                continue
        start_index = row.find(discon_string)
        if start_index != -1:
            mac = row[start_index + 1 + len(discon_string):].lstrip().rstrip()
            if mac in clients_connected:
                clients_connected.remove(mac)
    p = subprocess.Popen(['arp', '-a'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    output, stderrdata = p.communicate()
    output = output.decode('utf-8').split('\n')
    clients = []
    f = open(TEMP_DIR_NAME + 'hotspot.tmp', 'r')
    current_macs = f.readlines()
    f.close()
    for line in output:
        for i in range(len(clients_connected)):
            if clients_connected[i] in line:
                cl = Client(clients_connected[i], line.split()[0], '', AccessPoint.read_state()['essid'])
                if cl.mac not in current_macs:
                    cl.insert_info()
                    f = open(TEMP_DIR_NAME + 'hotspot.tmp', 'a')
                    f.writelines(cl.mac + '\n')
                    f.close()
                cl.get_my_nick()
                clients.append(cl)
    rows.reverse()
    return render_to_response("hostapd_logs.html", {'clients': clients, 'hostapd_log_rows': rows})


def start_hotspot(request):
    lg = Logging(LOGS_DIR_NAME + 'main.log')
    internal_interface = request.POST['host_iface']
    external_interface = request.POST['gate_iface']
    essid = request.POST['hs_essid']
    security = request.POST['hs_security']
    psk = request.POST['hs_psk']
    channel = 9
    lg.write_log('AP', 'host: {}, gate: {}, essid: {}, sec: {}, '
                       'psk: {}, channel: {}'.format(internal_interface, external_interface,
                                                     essid, security, psk, channel))
    if internal_interface == 'undefined' or external_interface == 'undefined' or security == 'undefined' or essid == '':
        lg.write_log('AP', 'Выбранны некорректные параметры')
        return render_to_response('ap_mode.html', {'ap_status': 0})
    ap = AccessPoint()
    ap.set_channel(channel)
    ap.set_essid(essid)
    ap.set_interface(internal_interface)
    ap.set_internet_interface(external_interface)
    if security != 'open':
        ap.set_psk(psk)
    try:
        ap.start()
    except Exception as ex:
        ap.on_exit()
        return render_to_response('ap_mode.html', {'ap_status': 0})
    return render_to_response('ap_mode.html', {'ap_status': 1})


def stop_hotspot(request):
    AccessPoint.on_exit()
    return render_to_response('ap_mode.html', {'ap_status': 0})
