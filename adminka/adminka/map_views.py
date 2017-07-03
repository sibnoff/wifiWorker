import json
from django.shortcuts import render_to_response
from adminka.source_code.constants import *
from adminka.source_code.mySqlWorker import MySqlWorker
from adminka.source_code.clientAndHotspot import Hotspot


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
