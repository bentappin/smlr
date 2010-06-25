from django.conf.urls.defaults import *
from django.conf import settings

from smlr.main.views import *


urlpatterns = patterns('',
	(r'^$', index),
	(r'^(\w+)$', reverse),
	(r'^(\d+)$', reverse),
	(r'^(\w+)\+$', stats),
)

if settings.SERVE_STATIC == True:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT}),
	)
