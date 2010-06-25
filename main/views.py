from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson

from smlr.main.models import URL, Redirect
from smlr.main.forms import URLForm
from smlr.main.utils import *


def index(request):
	url = None
	
	if request.method == 'POST':
		form = URLForm(request.POST)
		
		if form.is_valid():
			url = None
			
			if form.cleaned_data['alias']:
				url = URL.objects.create(	original_url=form.cleaned_data['long_url'],
											alias=form.cleaned_data['alias'],
											is_custom_alias=True)	
			else:
				try:
					url = URL.objects.filter(original_url=form.cleaned_data['long_url'], is_custom_alias=False)[0]
				except IndexError:
					pass
													
				if not url:
					url = URL.objects.create(original_url=form.cleaned_data['long_url'])

					potential_alias = base36encode(url.id)
					qs = URL.objects.filter(alias=potential_alias)
					counter = 1

					while qs:
						potential_alias = base36encode(url.id + counter)
						qs = URL.objects.filter(alias=potential_alias)
						counter += 1

					url.alias = potential_alias

			url.shortenings += 1
			url.save()
			
			long_url = form.cleaned_data['long_url']
			short_url = "http://" + request.META['HTTP_HOST'] + "/" + url.alias
	else:
		form = URLForm()
	
	return render_to_response('index.html', {
		'form': form,
		'url': url,
	})


def reverse(request, alias):
	try:
		url = URL.objects.get(alias=alias)
	except URL.DoesNotExist:
		return HttpResponseRedirect("/")
	
	redirect = Redirect()
	redirect.url = url
	redirect.user_agent = request.META.get('HTTP_USER_AGENT', None)
	redirect.remote_host = request.META.get('REMOTE_HOST', None)
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

	original_url = url.original_url
	short_url = url.get_short_url()
	
	reduction_chars = len(original_url) - len(short_url)
	reduction_percent = 100 - int(round((float(len(short_url)) /
								float(len(original_url))) * 100))
								
	redirects = url.redirect_set.count()
	shortenings = url.shortenings
	
	return render_to_response('stats.html', locals())
