from django.conf.urls.defaults import *
from smlr.main.views import *
from smlr import settings_local as settings

urlpatterns = patterns('',
	(r'^$', index),
	(r'^(\w+)$', reverse),
	(r'^(\d+)$', reverse),
	(r'^(\w+)\+$', stats),
	
)

if settings.DEBUG == True:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT}),
	)