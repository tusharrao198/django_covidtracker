from django.shortcuts import render
from .models import district_cases, states_cases
from django.db import models

# import os
# import psycopg2
import json
import ssl

# from pathlib import Path
import urllib.request, urllib.error

# from datetime import datetime

# ignoring ssl error
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url_daily = "https://api.rootnet.in/covid19-in/stats/latest"
# url2 = "https://api.rootnet.in/covid19-in/stats/history"
url_district = "https://api.covid19india.org/state_district_wise.json"


# function for opening url
def open_url(url_):
    try:
        fh = urllib.request.urlopen(url_, context=ctx)
        # .read() reads whole as a string
        data = fh.read().decode()
        js = json.loads(data)
        return js

    except:
        return "ERROR CONNECTING URL'S"


def update_state(url_, *args, **kwargs):
    try:
        js = open_url(url_)

        for i in js["data"]["regional"]:
            state_name_ = i["loc"]
            confirmed_ = i["totalConfirmed"]
            deaths_ = i["deaths"]
            recovered_ = i["discharged"]
            active_ = confirmed_ - (deaths_ + recovered_)

            # updating model

            # update_, created = states_cases.objects.get_or_create(state_name=state_name_)

            # to check condition if created we can do like:
            # if created:
            #     "do this"
            #     return pass
            changes = states_cases.objects.get(state_name=state_name_)
            if changes.confirmed != confirmed_:
                print("Updating model state_cases =", state_name_)
                do_it = states_cases(
                    state_name=state_name_,
                    confirmed=confirmed_,
                    Death=deaths_,
                    Recovered=recovered_,
                    Active=active_,
                )
                do_it.save()
            else:
                print(
                    f"{state_name_}--------------------------------------------cases are up to date"
                )

        return "success"

    except:
        return f"Error in update_district refresh page"


def update_district(url_):
    try:
        js1 = open_url(url_)
        for state in js1:
            state_name_ = state
            for cities in js1[state_name_]["districtData"]:
                city_name_ = cities
                confirmed_ = js1[state_name_]["districtData"][city_name_]["confirmed"]
                recovered_ = js1[state_name_]["districtData"][city_name_]["recovered"]
                active_ = js1[state_name_]["districtData"][city_name_]["active"]
                deaths_ = js1[state_name_]["districtData"][city_name_]["deceased"]

                changes = district_cases.objects.get(
                    state_name=state_name_, city_name=city_name_
                )
                if changes.confirmed != confirmed_:
                    print(
                        "Updating model district_cases =", state_name_, "->", city_name_
                    )
                    doit = district_cases(
                        state_name=state_name_,
                        city_name=city_name_,
                        confirmed=confirmed_,
                        Death=deaths_,
                        Recovered=recovered_,
                        Active=active_,
                    )
                    doit.save()
                else:
                    print(
                        f"{state_name_}-->{city_name_}----------------------district cases are up to date"
                    )
                    continue

            doit.save()
        return "success"

    except:
        return f"Error in update_district refresh page"


update_district(url_district)
update_state(url_daily)


# rendering home page
def covid_state(request):
    context_ = {
        "states_cases": states_cases.objects.all().order_by("id"),
        "title": "State",
        "state": "active",
    }
    return render(request, "covidtracker/home.html", context_)


# rendering district page
def covid_district(request):
    context_ = {
        "district_cases": district_cases.objects.all().order_by("id"),
        "title": "District",
        "district": "active",
    }
    return render(request, "covidtracker/district.html", context_)
