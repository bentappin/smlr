from django.conf.urls.defaults import *
from smlr.main.views import *
from smlr import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^yegg/', include('yegg.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

	(r'^$', index),
	(r'^(\w+)\+$', stats),
	(r'^(\w+)$', reverse),
	(r'^(\d+)$', reverse), # Account for 10, 11 etc.
	
)

if settings.DEBUG:
  urlpatterns += patterns('',
	# Dev static files
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',
	        {'document_root': settings.MEDIA_ROOT}),
  )
