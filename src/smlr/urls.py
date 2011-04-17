from django.conf.urls.defaults import *
from django.conf import settings

from smlr.main.views import *


urlpatterns = patterns('',
	url(r'^$', index),
	url(r'^(\w+)/$', reverse),
	url(r'^(\w+)\+/$', stats),
	url(r'^api/shorten/$', api_shorten),
	url(r'^api/stats/$', api_stats),
    url(r'^api/test/$', api_test),
)

if settings.SERVE_STATIC == True:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT}),
	)
