from django.conf.urls.defaults import *
from django.conf import settings

from smlr.main.views import *


urlpatterns = patterns('',
	url(r'^$', index),
	url(r'^(\w+)$', reverse),
	url(r'^(\d+)$', reverse),
	url(r'^(\w+)\+$', stats),
)

if settings.SERVE_STATIC == True:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT}),
	)
