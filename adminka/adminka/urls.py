from django.conf.urls import url
from adminka.views import settings, monitoring, hotspot, \
    sniff, jammer, proxy_server, rainbow_tables, map_working, \
    download, help_page, settings_save, settings_load, get_tail_log

urlpatterns = [
    url(r'^$', settings),
    url(r'^settings/$', settings),
    url(r'^settings/save/$', settings_save),
    url(r'^settings/load/$', settings_load),
    url(r'^get-logs/$', get_tail_log),
    url(r'^monitoring/$', monitoring),
    url(r'^hotspot/$', hotspot),
    url(r'^sniff/$', sniff),
    url(r'^jammer/$', jammer),
    url(r'^proxyserver/$', proxy_server),
    url(r'^rainbowtables/$', rainbow_tables),
    url(r'^mapworking/$', map_working),
    url(r'^download/$', download),
    url(r'^help/$', help_page)
]
