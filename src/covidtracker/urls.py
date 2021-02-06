from django.urls import path
from . import views

urlpatterns = [
    path("", views.covid_state, name="covid-home"),
    path("district", views.covid_district, name="district"),
]
