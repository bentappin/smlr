from django import forms
from django.forms.models import ValidationError

from smlr.main.models import URL


class URLForm(forms.Form):
	long_url = forms.URLField(label="Long URL")
	alias = forms.CharField(label="Custom shortname", max_length=8, required=False)
	
	def clean_alias(self):
		qs = URL.objects.filter(alias=self.cleaned_data['alias'])
		if qs and len(qs) > 0:
			raise ValidationError("Sorry! That smlr URL already exists.")
		return self.cleaned_data['alias']
