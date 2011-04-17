import re

from django import forms
from django.forms.models import ValidationError

from smlr.main.models import URL


class URLForm(forms.Form):
	long_url = forms.URLField(label="URL")
	alias = forms.CharField(label="Optional shortname", max_length=8, required=False)
	
	def clean_alias(self):
		alias = self.cleaned_data['alias']

		if alias and not re.compile('^\w*$').match(alias):
			raise ValidationError("Your shortname can only contain letters, numbers and the underscore.")
		
		qs = URL.objects.filter(alias=alias)
		if qs:
			raise ValidationError("Sorry! That smlr URL already exists.")
		
		return alias
