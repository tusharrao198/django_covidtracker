from django.contrib import admin
from .models import district_cases, states_cases, cases_inc


admin.site.register(states_cases)
admin.site.register(district_cases)
admin.site.register(cases_inc)