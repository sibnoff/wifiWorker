from django.conf.urls import url
from adminka.views import sniff, jammer, proxy_server, \
    rainbow_tables, download, help_page, get_tail_log
from adminka.settings_views import settings, settings_save, settings_load
from adminka.hotspot_views import hotspot, start_hotspot, stop_hotspot, hotspot_get_logs
from adminka.map_views import map_working, show_all_hotspot, hotspot_show, client_show
from adminka.monitoring_views import monitoring, monitoring_get_logs, stop_monitoring, start_monitoring

urlpatterns = [
    url(r'^$', settings),
    url(r'^settings/$', settings),
    url(r'^save-settings/$', settings_save),
    url(r'^load-settings/$', settings_load),
    url(r'^get-logs/$', get_tail_log),
    url(r'^monitoring/$', monitoring),
    url(r'^monitoring-get-logs/$', monitoring_get_logs),
    url(r'^hotspot/$', hotspot),
    url(r'^hostapd-get-logs/$', hotspot_get_logs),
    url(r'^start-monitor/$', start_monitoring),
    url(r'^stop-monitor/$', stop_monitoring),
    url(r'^stop-hotspot/$', stop_hotspot),
    url(r'^start-hotspot/$', start_hotspot),
    url(r'^sniff/$', sniff),
    url(r'^jammer/$', jammer),
    url(r'^proxyserver/$', proxy_server),
    url(r'^rainbowtables/$', rainbow_tables),
    url(r'^mapworking/$', map_working),
    url(r'^hotspot-show/$', hotspot_show),
    url(r'^client-show/$', client_show),
    url(r'^show-all-hotspot/$', show_all_hotspot),
    url(r'^download/$', download),
    url(r'^help/$', help_page)
]
