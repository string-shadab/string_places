from django.conf.urls import url

from . import views 

app_name = 'locations'
urlpatterns = [
    url(r'^$',views.load_cities,name='load_city'),
    url(r'^load_in_db/$',views.load_in_db,name='load_in_db'),
]