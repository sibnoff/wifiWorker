from django.conf.urls import url
from adminka.views import settings, monitoring, hotspot, \
    sniff, jammer, proxy_server, rainbow_tables, map_working, \
    download, help_page, settings_save, settings_load, get_tail_log, \
    show_all_hotspot, hotspot_show, client_show

urlpatterns = [
    url(r'^$', settings),
    url(r'^settings/$', settings),
    url(r'^save-settings/$', settings_save),
    url(r'^load-settings/$', settings_load),
    url(r'^get-logs/$', get_tail_log),
    url(r'^monitoring/$', monitoring),
    url(r'^hotspot/$', hotspot),
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
