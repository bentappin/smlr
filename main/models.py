from django.db import models

class URL(models.Model):
	original_url= models.URLField()
	redirects = models.IntegerField(default=0)
	shortenings = models.IntegerField(default=0)
	last_redirect = models.DateTimeField(null=True)
	created = models.DateTimeField(null=True, blank=True, auto_now_add=True)
	mapping = models.CharField(max_length=8, null=True, blank=True)
	
	def to_dict(self):
		return { "original_url": str(self.original_url), "redirects": int(self.redirects), "shortenings": int(self.shortenings) }