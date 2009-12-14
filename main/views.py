from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson

from smlr.main.forms import URLForm
from smlr.main.models import URL, Redirect
from smlr.main.utils import *

from datetime import datetime

def index(request):
	long_url = ""
	short_url = ""
	
	if request.method == 'POST':
		form = URLForm(request.POST)
		if form.is_valid():
			qs = URL.objects.filter(original_url=form.cleaned_data['long_url'])
			
			if qs:
				url = qs[0]
			else:
				url = URL.objects.create(original_url=form.cleaned_data['long_url'])
				
			url.alias = base36encode(url.id)
			url.shortenings += 1
			url.save()
			
			long_url = form.cleaned_data['long_url']
			short_url = request.META['wsgi.url_scheme'] + "://" + request.META['HTTP_HOST'] + "/" + url.alias
	else:
		form = URLForm()
	
	return render_to_response('index.html', {'form':form, 'long_url': long_url, 'short_url': short_url})

def reverse(request, alias):
	try:
		url = URL.objects.get(alias=alias)
	except:
		return HttpResponseRedirect("/")
	
	redirect = Redirect()
	redirect.url = url
	redirect.user_agent = request.META.get('HTTP_USER_AGENT', None)
	redirect.remote_ip = request.META.get('REMOTE_ADDR', None)
	redirect.remote_port = request.META.get('REMOTE_PORT', None)
	redirect.request_method = request.META.get('REQUEST_METHOD', None)
	redirect.save()
	
	return HttpResponseRedirect(url.original_url)

def stats(request, alias):
	try:
		url = URL.objects.get(alias=alias)
	except:
		return HttpResponseRedirect("/")

	data = {}
	data["original_url"] = url.original_url
	data["short_url"] = request.META['wsgi.url_scheme'] + "://" + request.META['HTTP_HOST'] + "/" + url.alias
	data["reduction_chars"] = len(data["original_url"]) - len(data["short_url"])
	data["reduction_percent"] = 100 - int(round((float(len(data["short_url"])) / float(len(data["original_url"]))) * 100))
	data["redirects"] = url.redirect_set.count()
	return render_to_response('stats.html', data)
