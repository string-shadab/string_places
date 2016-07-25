from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class Cities(models.Model):
    name = models.CharField(max_length = 100)
    check = models.BooleanField(default = False)
    recordfound = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Continent(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Country(models.Model):
    continent = models.ForeignKey(Continent, blank=True, null=True)
    name = models.CharField(max_length=200, unique = True)

    def __str__(self):
        return self.name

class Division(models.Model):
    country = models.ForeignKey(Country, blank=True, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Subdivision(models.Model):
    division = models.ForeignKey(Division, blank=True, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Place(models.Model):
    subdivision = models.ForeignKey(Subdivision, blank=True, null=True)
    name = models.CharField(max_length=200)
    place_id = models.CharField(max_length=50)


    def __str__(self):
        return self.name
