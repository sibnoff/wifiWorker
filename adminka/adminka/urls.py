"""adminka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
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
