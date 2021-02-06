from django.urls import path
from . import views

urlpatterns = [
    path("", views.covid_state, name="covid-home"),
    path("covidtracker/district", views.covid_district, name="district"),
    path("covidtracker/search", views.search, name="search"),
    path("covidtracker/<str:s_name>/", views.each_state, name="city"),
]
