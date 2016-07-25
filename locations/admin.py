from django.contrib import admin

from .models import Cities
from import_export import resources

class CityNames(resources.ModelResource):
    class Meta:
        model = Cities

class CityResources(resources.ModelResource):
    class Meta:
        model = Cities
        fields = ('name',) 