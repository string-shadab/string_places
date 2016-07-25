from django.conf.urls import url

from . import views 

app_name = 'locations'
urlpatterns = [
    url(r'^loadcities/$',views.load_cities,name='load_city'),
    url(r'^load_in_db/$',views.load_in_db,name='load_in_db'),
    url(r'^download/city/$',views.city_in_file,name='city'),
    url(r'^download/cityinfo/$',views.city_info_in_file,name='cityinfo'),
    url(r'^getcities/$',views.get_cities,name = 'getcities'),
]