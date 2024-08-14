from django.urls import path
from . import views

urlpatterns = [
    path('',views.scraping,name ='scraping'),
    path('zillow/',views.run_spiders, name='zillow'),
    path('airbnb/',views.airbnb, name='airbnb'),
    path('data_mapping/',views.data_mapping, name='data_mapping'),

   
]