from django.shortcuts import render
from django.http import HttpResponse
import tablib
from import_export import resources
from locations.models import Cities

def load_cities(request):
    return render(request,'locations/load_cities.html',{})

def load_in_db(request):
    

    file = open(request.POST['file'])
    filedata = file.read()
   
    city_resource = resources.modelresource_factory(model=Cities)()
    dataset = tablib.Dataset()
    dataset.load(open(request.POST['file']).read())
     
    result = city_resource.import_data(dataset,dry_run=False)
    return HttpResponse('Done..!!') 