from django.shortcuts import render
from django.db.models import Avg, Count, Min, Sum
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.core import serializers
from .models import district_cases, states_cases, cases_inc
from django.db import models
import json
import ssl
import urllib.request, urllib.error
import requests
from datetime import datetime as dt

# ignoring ssl error
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# function for opening url
def open_url(url_):
    try:
        res = requests.get(url_)
        js = res.json()
        return js

    except:
        fh = urllib.request.urlopen(url_, context=ctx)
        # .read() reads whole as a string
        data = fh.read().decode()
        js = json.loads(data)
        return js


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


# Cases Increment
def cases_increment():
    url_history = "https://api.rootnet.in/covid19-in/stats/history"
    js2 = open_url(url_history)
    data = list(js2["data"])
    before = data[-2]["summary"]
    present = data[-1]["summary"]
    before_date = data[-2]["day"]
    present_date = data[-1]["day"]
    cases = {
        present_date: {
            "total": present["total"],
            "deaths": present["deaths"],
            "discharged": present["discharged"],
        },
        before_date: {
            "total": before["total"],
            "deaths": before["deaths"],
            "discharged": before["discharged"],
        },
    }

    inc = {
        "cases_inc": cases[present_date]["total"] - cases[before_date]["total"],
        "day_before": before_date,
        "present_date": present_date,
        "death_inc": cases[present_date]["deaths"] - cases[before_date]["deaths"],
        "recovered_inc": cases[present_date]["discharged"]
        - cases[before_date]["discharged"],
    }
    confirmed_inc_ = str(cases_inc.objects.get(confirmed_inc=inc["cases_inc"]))
    day_before_ = str(cases_inc.objects.get(date_before=inc["day_before"]))
    present_date_ = str(cases_inc.objects.get(present_date=inc["present_date"]))
    death_inc_ = str(cases_inc.objects.get(death_inc=inc["death_inc"]))
    recovered_inc_ = str(cases_inc.objects.get(recovered_inc=inc["recovered_inc"]))

    if (day_before_ == str(inc["day_before"])) or (
        present_date_ == str(inc["present_date"])
    ):
        doit = cases_inc.objects.filter().update(
            confirmed_inc=inc["cases_inc"],
            date_before=inc["day_before"],
            present_date=inc["present_date"],
            death_inc=inc["death_inc"],
            recovered_inc=inc["recovered_inc"],
        )


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

            if city_name_ != f"Unknown":
                try:
                    changes = district_cases.objects.filter(city_name=city_name_)
                    if confirmed_ > changes[0].confirmed:
                        # print(
                        #     "Updating model district_cases =", state_name_, "->", city_name_
                        # )
                        do_it = district_cases.objects.filter(
                            city_name=city_name_
                        ).update(
                            state_name=state_name_,
                            city_name=city_name_,
                            confirmed=confirmed_,
                            Death=deaths_,
                            Recovered=recovered_,
                            Active=active_,
                        )
                        # do_it.save()
                except:
                    pass

            elif city_name_ == f"Unknown":
                city_name_ = f"{city_name_}+{state_name_}"
                try:
                    changes = district_cases.objects.filter(city_name=city_name_)
                except:
                    changes = district_cases.objects.filter(
                        city_name=f"Unknown+{state_name_}"
                    )
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
            # else:
            #     print(
            #         f"{state_name_}---->{city_name_}----------------------district cases are up to date"
            #     )


date_ = str(dt.now()).split()[0]
dated1 = str(district_cases.objects.values("Dated")[0]["Dated"])
dated2 = str(cases_inc.objects.values("Dated")[0]["Dated"])
dated3 = str(states_cases.objects.values("Dated")[0]["Dated"])

# updating if changes made, only for the first user goes to a site

##################################################################################
# Views
# rendering home page
def covid_state(request):
    if dated3 != date_:
        update_state()
    if dated2 != date_:
        cases_increment()

    confirmed_inc = cases_inc.objects.values("confirmed_inc")[0]
    present_date = cases_inc.objects.values("present_date")[0]
    death_inc = cases_inc.objects.values("death_inc")[0]
    recovered_inc = cases_inc.objects.values("recovered_inc")[0]
    # print("recovered_inc", recovered_inc)

    confirmed__sum = states_cases.objects.all().aggregate(Sum("confirmed"))
    Active__sum = states_cases.objects.all().aggregate(Sum("Active"))
    Recovered__sum = states_cases.objects.all().aggregate(Sum("Recovered"))
    Death__sum = states_cases.objects.all().aggregate(Sum("Death"))
    context_ = {
        "confirmed": confirmed__sum["confirmed__sum"],
        "Active": Active__sum["Active__sum"],
        "Death": Death__sum["Death__sum"],
        "Recovered": Recovered__sum["Recovered__sum"],
        "district_cases": district_cases.objects.all(),
        "states_cases": states_cases.objects.all().order_by("id"),
        "cases_increment": confirmed_inc["confirmed_inc"],
        "recovered_inc": recovered_inc["recovered_inc"],
        "death_inc": death_inc["death_inc"],
        # "day_before": day_before,
        "present_date": present_date["present_date"],
        "title": "INDIA",
        "state": "active",
    }
    return render(request, "covidtracker/home.html", context_)


# rendering district page
def covid_district(request):
    if dated1 != date_:
        update_district()
        print("UPDAAAAAA")
    else:
        print("FASLSEV")
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
    if str(city_query) == "Unknown":
        city_query = f"Unknown+{state_query}"
        city_cases = district_cases.objects.filter(
            state_name=state_query, city_name=city_query
        )
    else:
        city_cases = district_cases.objects.filter(
            state_name=state_query, city_name=city_query
        )

    # a = list(city_cases)
    # city_json = district_cases.objects.filter(
    #     state_name=state_query, city_name=city_query
    # ).first()  # .first() convert object to instance)

    #  {'id': 983, 'city_name': 'Mandi', 'state_name': 'Himachal Pradesh', 'confirmed': 10096, 'Death': 124, 'Recovered': 9786, 'Active': 182}
    # city_json = model_to_dict(city_json)
    context_ = {
        "query_results": city_cases,
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
        raise Http404("State_query does not exist")

    context_ = {
        "title": city_title,
        "city": "active",
        "state_query": state_query,
        "state_data": state_data,
        "state_total_cases": state_total_cases,
    }
    return render(request, "covidtracker/city.html", context_)
