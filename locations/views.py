from django.shortcuts import render
from django.http import HttpResponse
import tablib
import csv
from import_export import resources
from locations.models import Cities,Continent,Country,Division,Subdivision,Place
from locations.admin import CityResources
import json
import time
import httplib
import thread


def city_info_in_file(request):
    all_places = Place.objects.all()
    data = ''
    for place in all_places:
        data = data + place.name + ','+ place.subdivision.name + ',' + place.subdivision.division.name + ',' + place.subdivision.division.country.name + '\n'  
    response = HttpResponse(content_type = 'text/plain')
    response['Content-Disposition'] = 'attachment;filename="citiesinfo.txt"'
    response.write(data)
    return response

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

def city_in_file(request):
    data = CityResources().export()
    print data
    response = HttpResponse(content_type = 'text/plain')
    response['Content-Disposition'] = 'attachment;filename="cities.txt"'
    response.write(data)
    return response

def get_cities(request):
    conn = httplib.HTTPSConnection("maps.googleapis.com")
    key='AIzaSyCYXfKbR-ufOMPZOnrkCgbRjAWBX-_jAXU'  
    all_places  = Cities.objects.filter(check = False)
    city_info = []
    for place in all_places:
        result = get_place(place.name,conn,key)
        if(result == 'break'):
            break;
        place.check = True
        if(result!=None and result != [] ):
            place.recordfound = True
        place.save()
        city_info.append(result)
    return HttpResponse(city_info)

def get_place(place,conn,key):
    """
    This function will fetch city IDs from a list of cities stored in a file, then will pass
    those city IDs to another function get_city_info() which will fetch other details about that
    city based on the ID.
    """
    place = place.replace(' ','%20')
    url='/maps/api/place/autocomplete/json?input='+place+'&types=(cities)&key=' +key
    conn.request("GET", url)
    response1 = conn.getresponse()
    response2 = response1.read()
    json_obj=json.loads(response2)
    if json_obj['status'] == "OK":
        data = []
    	for i in json_obj['predictions']:
            terms=i['terms']
            country=terms[len(terms)-1]
            c=country['value']
            if c=='India':
                place_id=i['place_id']
                place=get_city_info(place_id,conn,key)
                if(place == None):
                    return 'break'
                data.append(place)
        return data
    elif json_obj['status'] == 'ZERO_RESULTS':
        return None
    else:
        return 'break';


def get_city_info(place_id,conn,key):
    """
    This function will fetch details about a city based on a city ID passed to it as parameter
    """
    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + place_id + '&key=' + key
    conn.request("GET", url)
    response1 = conn.getresponse()
    response2 = response1.read()
    json_obj = json.loads(response2)
    print json_obj
    if(json_obj['status'] == 'OK'):
        data  = json_obj['result']['address_components']
        info = []
        for i in range(4):
            info.append(data[i]['long_name'])
        info.append(place_id)
        try:
            store_in_file(place_id+'.json',json_obj)
        except Exception:
            pass
    
        store_in_db(info)
        return(info)
    elif(json_obj['status'] == 'OVER_QUERY_LIMIT'): 
        return None
    
    

def store_in_db(place_info):
    country = Country.objects.filter(name = place_info[3])
    country_len = len(country)
    if(country_len==0):
        country = Country(name = place_info[3])
        country.save()
    if(country_len==1):
        divisions = country[0].division_set.all()
        flag = False
        division = 1
        for div in divisions:
            if(div.name == place_info[2]):
                flag=True
                division = div
                break;
        if(flag==False):
            division = Division(name = place_info[2])
            division.country = country[0]
            division.save()

        subdivisions = division.subdivision_set.all()
        flag = False
        subdivision = 1
        for subdiv in subdivisions:
            if(subdiv.name == place_info[1]):
                flag = True
                subdivision = subdiv
                break;
        if(flag==False):
            subdivision = Subdivision(name = place_info[1])
            subdivision.division = division
            subdivision.save()
        
        place = Place(name = place_info[0],place_id = place_info[4])
        place.subdivision = subdivision
        place.save()

def store_in_file(file_name,data):
    file_loc = 'locations\\data\\'+file_name 
    with open(file_loc, mode="wb+") as file:
        json.dump(data,file)


    