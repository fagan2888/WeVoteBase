# wevotebase/urls.py
# Brought to you by We Vote. Be good.
# -*- coding: UTF-8 -*-

"""
wevotebase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static  # Django cookbook
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # Django cookbook

from wevotebase import views

urlpatterns = patterns(
    '',
    url(r'^$', views.start_view, name='start',),
    url(r'^myb/', include('ux_oak.urls', namespace="my_ballot")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^import_export/', include('import_export.urls', namespace="import_export")),
    url(r'^import_export_google_civic/', include(
        'import_export_google_civic.urls', namespace="import_export_google_civic")),
    url(r'^import_export_theunitedstatesio/', include(
        'import_export_theunitedstatesio.urls', namespace="import_export_theunitedstatesio")),
    url(r'^org/', include('organization.urls', namespace="organization")),
    url(r'^politician_list/', include('politician.urls', namespace="politician_list")),
    url(r'^politician/', include('politician.urls', namespace="politician")),
    url(r'^pos/', include('position.urls', namespace="position")),
    url(r'^sod/', include('support_oppose_deciding.urls', namespace="support_oppose_deciding")),
    url(r'^tag/', include('tag.urls', namespace="tag")),
    # Django cookbook
    url(r'^js-settings/$', 'utils.views.render_js', {'template_name': 'settings.js'}, name="js_settings"),
)

urlpatterns += staticfiles_urlpatterns()  # Django Cookbook
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Django Cookbook
