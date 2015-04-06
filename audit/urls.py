try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    url(r'^upload/?', 'audit.views.upload', name='upload'),
    url(r'^save_audit/?', 'audit.views.save_audit', name='save_audit'),
)
