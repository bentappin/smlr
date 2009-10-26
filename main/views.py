from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson

from smlr.main.forms import URLForm
from smlr.main.models import URL
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
				
			url.mapping = base36encode(url.id)
			url.shortenings += 1
			url.save()
			
			long_url = form.cleaned_data['long_url']
			short_url = request.META['wsgi.url_scheme'] + "://" + request.META['HTTP_HOST'] + "/" + url.mapping
	else:
		form = URLForm()
	
	return render_to_response('index.html', {'form':form, 'long_url': long_url, 'short_url': short_url})
	
def reverse(request, alias):
	qs = URL.objects.filter(mapping=alias)
	if len(qs) != 1:
		return HttpResponseRedirect("/")
		
	url = qs[0]
	url.redirects += 1
	url.last_redirect = datetime.now()
	url.save()
	return HttpResponseRedirect(url.original_url)

def stats(request, alias):
	qs = URL.objects.filter(mapping=alias)
	if len(qs) != 1:
		return HttpResponseRedirect("/")

	url = qs[0]
	
	data = url.to_dict()
	data["short_url"] = request.META['wsgi.url_scheme'] + "://" + request.META['HTTP_HOST'] + "/" + url.mapping
	data["reduction_chars"] = len(data["original_url"]) - len(data["short_url"])
	data["reduction_percent"] = 100 - int(round((float(len(data["short_url"])) / float(len(data["original_url"]))) * 100))
	print data
	return render_to_response('stats.html', data)
