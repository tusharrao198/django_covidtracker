from django.db.models import Avg, Min, Max, Count, Sum
from .models import district_cases, states_cases, CasesIncrementCheck
import ssl, json
from datetime import datetime as dt
import urllib.request
import urllib.error
import requests

# from django.db.models import Avg, Count, Min
# from django.core.serializers.json import DjangoJSONEncoder
# from django.forms.models import model_to_dict
# from django.core import serializers
# from django.db import models

date_ = str(dt.now()).split()[0]


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


confirmed__sum_before = states_cases.objects.all().aggregate(Sum("confirmed"))[
    "confirmed__sum"
]
Active__sum_before = states_cases.objects.all().aggregate(Sum("Active"))[
    "Active__sum"]
Recovered__sum_before = states_cases.objects.all().aggregate(Sum("Recovered"))[
    "Recovered__sum"
]
Death__sum_before = states_cases.objects.all().aggregate(Sum("Death"))[
    "Death__sum"]
date_before = str(states_cases.objects.values("Dated")[0]["Dated"])



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
            print("Updating.... model state_cases =", state_name_)
            do_it = states_cases.objects.filter(state_name=state_name_).update(
                state_name=state_name_,
                confirmed=confirmed_,
                Death=deaths_,
                Recovered=recovered_,
                Active=active_,
                Dated=date_,
            )
        states_cases.objects.filter(state_name=state_name_).update(
            Dated=date_,
        )
        # do_it.save()
        # else:
        #     print(
        #         f"{state_name_}--------------------------------------------cases are up to date"
        #     )




# Cases Increment
def cases_increment():
    # total cases after _updating
    confirmed__sum_after = states_cases.objects.all().aggregate(Sum("confirmed"))[
        "confirmed__sum"
    ]
    Active__sum_after = states_cases.objects.all().aggregate(Sum("Active"))[
        "Active__sum"
    ]
    Recovered__sum_after = states_cases.objects.all().aggregate(Sum("Recovered"))[
        "Recovered__sum"
    ]
    Death__sum_after = states_cases.objects.all().aggregate(Sum("Death"))[
        "Death__sum"]

    date_after = str(states_cases.objects.values("Dated")[0]["Dated"])
    print(f"DATE AFTER = {date_after}")

    inc = {
        "totalcases_inc": confirmed__sum_after - confirmed__sum_before,
        "day_before": date_before,
        "present_date": date_after,
        "death_inc": Death__sum_after - Death__sum_before,
        "recovered_inc": Recovered__sum_after - Recovered__sum_before,
    }

    query1 = CasesIncrementCheck.objects.all().first()
    confirmed_inc_ = query1.confirmed_inc
    death_inc = query1.death_inc
    recovered_inc = query1.recovered_inc
    day_before_ = query1.date_before
    present_date_ = query1.present_date

    doit = CasesIncrementCheck.objects.filter(present_date=present_date_).update(
        confirmed_inc=inc["totalcases_inc"],
        date_before=inc["day_before"],
        present_date=inc["present_date"],
        death_inc=inc["death_inc"],
        recovered_inc=inc["recovered_inc"],
        Dated=date_after,
    )
    print(f"DATA UPDATED in CasesIncrementCheck")


# district cases updation
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
                    changes = district_cases.objects.filter(
                        city_name=city_name_)
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
                    district_cases.objects.filter(city_name=city_name_).update(
                        Dated=date_,
                    )
                except:
                    pass

            elif city_name_ == f"Unknown":
                city_name_ = f"{city_name_}+{state_name_}"
                try:
                    changes = district_cases.objects.filter(
                        city_name=city_name_)
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
                district_cases.objects.filter(city_name=city_name_).update(
                    Dated=date_,
                )
            # else:
            #     print(
            #         f"{state_name_}---->{city_name_}----------------------district cases are up to date"
            #     )
