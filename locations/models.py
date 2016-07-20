from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class Cities(models.Model):
	name = models.CharField(max_length = 100)

	def __unicode__(self):
    		return self.name
