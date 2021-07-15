from django.contrib import admin
from .models import *

admin.site.register(states_cases)
admin.site.register(district_cases)
admin.site.register(CasesIncrementCheck)
admin.site.register(About)

# try:

# except:
#     print("Skipping Warning No module named 'covidtracker.models' in admin.py")
#     pass
