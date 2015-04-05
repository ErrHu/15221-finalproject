from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'cmuaudit.views.home', name='home'),
    url(r'^sign_in/?', 'cmuaudit.views.sign_in', name='sign_in'),
    url(r'^sign_up/?', 'cmuaudit.views.sign_up', name='sign_up'),
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^audit/', include('audit.urls', app_name='audit'))
)
