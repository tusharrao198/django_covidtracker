from django.shortcuts import render

from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.core import serializers
from .models import district_cases, states_cases
from django.db import models
from .filters import search_
import json
import ssl
import urllib.request, urllib.error

# import os
# import psycopg2
# from pathlib import Path
# from datetime import datetime

# ignoring ssl error
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# url2 = "https://api.rootnet.in/covid19-in/stats/history"

# function for opening url
def open_url(url_):
    try:
        fh = urllib.request.urlopen(url_, context=ctx)
        # .read() reads whole as a string
        data = fh.read().decode()
        js = json.loads(data)
        return js

    except:
        return open_url(url_)


def update_state():
    url_daily = "https://api.rootnet.in/covid19-in/stats/latest"
    js = open_url(url_daily)
    for i in js["data"]["regional"]:
        state_name_ = i["loc"]
        confirmed_ = i["totalConfirmed"]
        deaths_ = i["deaths"]
        recovered_ = i["discharged"]
        active_ = confirmed_ - (deaths_ + recovered_)

        # updating models
        changes = states_cases.objects.filter(state_name=state_name_)
        if confirmed_ > changes[0].confirmed:
            # print("Updating.... model state_cases =", state_name_)
            do_it = states_cases.objects.filter(state_name=state_name_).update(
                state_name=state_name_,
                confirmed=confirmed_,
                Death=deaths_,
                Recovered=recovered_,
                Active=active_,
            )
            # do_it.save()
        # else:
        #     print(
        #         f"{state_name_}--------------------------------------------cases are up to date"
        #     )


def totalcases_count():
    url_daily = "https://api.rootnet.in/covid19-in/stats/latest"
    js = open_url(url_daily)
    return js["data"]["summary"]["total"]

# Cases Increment 
def cases_increment():
    Totalcases = totalcases_count()
    url_history = "https://api.rootnet.in/covid19-in/stats/history"
    js2 = open_url(url_history)
    print("making connection")
    # cases incement of last two days in  INDIA
    dict_inc={}
    for i in range(len(js2['data'])):
      #info_datewise = i
      if i >= (len(js2['data'])-2):
          cases_state = [js2['data'][i]['summary']['total'], js2['data'][i]['summary']['deaths'], js2['data'][i]['summary']['discharged']]
          dict_inc[js2['data'][i]['day']] = cases_state
    # finding increase in cases per day
    len_dict = len(list(dict_inc))
    day_before = list(dict_inc)[0]
    present_date = list(dict_inc)[1]
    print("day_before: ",day_before)
    print("last: ",present_date)
    inc = dict_inc[present_date][0]-dict_inc[day_before][0]
    print("inc: ", inc)
    return inc, day_before, present_date

increment, day_before, present_date = cases_increment()

def update_district():
    url_district = "https://api.covid19india.org/state_district_wise.json"
    js1 = open_url(url_district)
    for state in js1:
        state_name_ = state
        for cities in js1[state_name_]["districtData"]:
            city_name_ = cities
            confirmed_ = js1[state_name_]["districtData"][city_name_]["confirmed"]
            recovered_ = js1[state_name_]["districtData"][city_name_]["recovered"]
            active_ = js1[state_name_]["districtData"][city_name_]["active"]
            deaths_ = js1[state_name_]["districtData"][city_name_]["deceased"]
            # if city_name_=="Unknown": print(f"Unknown+{state_name_}")

            if city_name_!=f"Unknown+{state_name_}":
                # print("THISone , if city_name_!=:")
                try:
                    changes = district_cases.objects.filter(city_name=city_name_)
                    print("TRY : ", changes)
                    print("\n\nFROM ---------------DB=========================    ",changes)
                    print("\n\nFROM DB=========================    ",changes[0].confirmed)
                    print("\n\nnew-confirmed =--------------  ",confirmed_)
                    if confirmed_ > changes[0].confirmed:
                        # print(
                        #     "Updating model district_cases =", state_name_, "->", city_name_
                        # )
                        do_it = district_cases.objects.filter(city_name=city_name_).update(
                            state_name=state_name_,
                            city_name=city_name_,
                            confirmed=confirmed_,
                            Death=deaths_,
                            Recovered=recovered_,
                            Active=active_,
                        )
                except:
                    city_name_= f"Unknown+{state_name_}"
                    changes = district_cases.objects.filter(city_name=city_name_)
                    print("EXCEPT : ", changes)
                    print("\n\nFROM ---------------DB=========================    ",changes)
                    print("\n\nFROM DB=========================    ",changes[0].confirmed)
                    print("\n\nnew-confirmed =--------------  ",confirmed_)
                    if confirmed_ > changes[0].confirmed:
                        # print(
                        #     "Updating model district_cases =", state_name_, "->", city_name_
                        # )
                        do_it = district_cases.objects.filter(city_name=city_name_).update(
                            state_name=state_name_,
                            city_name=city_name_,
                            confirmed=confirmed_,
                            Death=deaths_,
                            Recovered=recovered_,
                            Active=active_,
                        )
            
            elif city_name_==f"Unknown+{state_name_}":
                print("THISone , if city_name_==:")
                city_name_ = f"{city_name_}+{state_name_}"
                try:
                    changes = district_cases.objects.filter(city_name=city_name_)
                except:
                    changes = district_cases.objects.filter(city_name=f"Unknown+{state_name_}")
                # changes = district_cases.objects.filter(city_name=f"{city_name_}+{state_name_}")
                print("\n\nFROM ---------------DB=========================    ",changes)
                print("\n\nFROM DB=========================    ",changes[0].confirmed)
                print("\n\nnew-confirmed =--------------  ",confirmed_)
                if confirmed_ > changes[0].confirmed:
                    # print(
                    #     "Updating model district_cases =", state_name_, "->", city_name_
                    # )
                    
                    do_it = district_cases.objects.filter(city_name=city_name_).update(
                        state_name=state_name_,
                        city_name=city_name_,
                        confirmed=confirmed_,
                        Death=deaths_,
                        Recovered=recovered_,
                        Active=active_,
                    )
 
                # do_it.save()
            # else:
            #     print(
            #         f"{state_name_}---->{city_name_}----------------------district cases are up to date"
            #     )


# update_state()
# update_district()
# updating if changes made, only for the first user goes to a site

##################################################################################
# Views
# rendering home page
def covid_state(request):
    # citycases = states_cases.objects.all()
    # query = search_(request.GET, queryset=citycases)
    # citycases = query.qs
    context_ = {
        # "city_cases": "city_cases",
        "Totalcases": totalcases_count(),
        "district_cases": district_cases.objects.all(),
        "states_cases": states_cases.objects.all().order_by("id"),
        "title": "State",
        "state": "active",
        "increment": increment,
        "day_before": day_before,
        "present_date": present_date,
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


# rendering search page
def search(request):
    state_query = request.GET["state"]
    city_query = request.GET["city"]
    # print(f"{state_query} - >> {city_query}")
    city_cases = district_cases.objects.filter(
        state_name=state_query, city_name=city_query
    )
    a = list(city_cases)
    city_json = district_cases.objects.filter(
        state_name=state_query, city_name=city_query
    ).first()  # .first() conveerts object to instance)

    #  {'id': 983, 'city_name': 'Mandi', 'state_name': 'Himachal Pradesh', 'confirmed': 10096, 'Death': 124, 'Recovered': 9786, 'Active': 182}

    city_json = model_to_dict(city_json)
    # print(city_json)
    context_ = {
        "query_results": city_cases,
        "city_json": "city_json",
        "title": "Result",
        "search": "active",
    }
    return render(request, "covidtracker/search.html", context_)


def each_state(request, s_name):
    try:
        # question = Question.objects.get(pk=question_id)
        state_query = states_cases.objects.get(state_name=s_name)
        state_total_cases = states_cases.objects.get(state_name=s_name)
        state_data = district_cases.objects.filter(state_name=state_query)
        city_title = state_total_cases.state_name
    except state_query.DoesNotExist:
        raise Http404("Question does not exist")
    context_ = {
        # "city": district_cases.objects.filter(state_name=state_query),
        "title": city_title,
        "city": "active",
        "state_query": state_query,
        "state_data": state_data,
        "state_total_cases": state_total_cases,
    }
    return render(request, "covidtracker/city.html", context_)
