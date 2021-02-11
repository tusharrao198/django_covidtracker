from covidtracker.models import district_cases, states_cases, CasesIncrementCheck
from django.db.models import Avg, Count, Min, Sum
from django.db import models
import json
import ssl
import urllib.request, urllib.error
import requests
from datetime import datetime as dt

date_ = str(dt.now()).split()[0]

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
        res = requests.get(url_)
        js = res.json()
        return js

    except:
        fh = urllib.request.urlopen(url_, context=ctx)
        # .read() reads whole as a string
        data = fh.read().decode()
        js = json.loads(data)
        return js


def update_state(url_, *args, **kwargs):
    try:
        js = open_url(url_)
        states_cases.objects.all().delete()
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
            print("Updation =", state_name_)
            do_it = states_cases(
                state_name=state_name_,
                confirmed=confirmed_,
                Death=deaths_,
                Recovered=recovered_,
                Active=active_,
                Dated=date_,
            )
            do_it.save()
    except:
        return "Error in update_district func"


def update_district(url_):
    # try:
    js1 = open_url(url_)
    district_cases.objects.all().delete()
    for state in js1:
        state_name_ = state
        for cities in js1[state_name_]["districtData"]:
            city_name_ = cities
            confirmed_ = js1[state_name_]["districtData"][city_name_]["confirmed"]
            recovered_ = js1[state_name_]["districtData"][city_name_]["recovered"]
            active_ = js1[state_name_]["districtData"][city_name_]["active"]
            deaths_ = js1[state_name_]["districtData"][city_name_]["deceased"]

            ####################################################

            ####################################################
            # changes = district_cases.objects.filter(
            #    state_name=state_name_, city_name=city_name_
            # )
            # print("CHANGES,", changes)
            # if changes==confirmed_
            #     print("Updating District_cases =", state_name_, city_name_)
            if city_name_ == "Unknown":
                city_name_ = f"{city_name_}+{state_name_}"
                try:
                    changes = district_cases.objects.filter(
                        city_name=city_name_, state_name=state_name_
                    )
                    # print("changes",changes)
                    if changes[0].city_name != city_name_:
                        print(
                            "Updating District_cases =",
                            state_name_,
                            " --->",
                            city_name_,
                        )
                        doit = district_cases(
                            state_name=state_name_,
                            city_name=city_name_,
                            confirmed=confirmed_,
                            Death=deaths_,
                            Recovered=recovered_,
                            Active=active_,
                            Dated=date_,
                        )
                        doit.save()
                except:
                    print("Updating District_cases =", state_name_, " --->", city_name_)
                    doit = district_cases(
                        state_name=state_name_,
                        city_name=city_name_,
                        confirmed=confirmed_,
                        Death=deaths_,
                        Recovered=recovered_,
                        Active=active_,
                        Dated=date_,
                    )
                    doit.save()

            else:
                try:
                    changes = district_cases.objects.filter(
                        city_name=city_name_, state_name=state_name_
                    )
                    # print("changes",changes)
                    if changes[0].city_name != city_name_:
                        print(
                            "Updating District_cases =",
                            state_name_,
                            " --->",
                            city_name_,
                        )
                        doit = district_cases(
                            state_name=state_name_,
                            city_name=city_name_,
                            confirmed=confirmed_,
                            Death=deaths_,
                            Recovered=recovered_,
                            Active=active_,
                            Dated=date_,
                        )
                        doit.save()
                except:
                    print("Updating District_cases =", state_name_, " --->", city_name_)
                    doit = district_cases(
                        state_name=state_name_,
                        city_name=city_name_,
                        confirmed=confirmed_,
                        Death=deaths_,
                        Recovered=recovered_,
                        Active=active_,
                        Dated=date_,
                    )
                    doit.save()

        doit.save()


# except:
#     return "Error in update_district func"


# # Cases Increment
# def cases_increment():
#     confirmed__sum_after = states_cases.objects.all().aggregate(Sum("confirmed"))[
#         "confirmed__sum"
#     ]
#     Active__sum_after = states_cases.objects.all().aggregate(Sum("Active"))[
#         "Active__sum"
#     ]
#     Recovered__sum_after = states_cases.objects.all().aggregate(Sum("Recovered"))[
#         "Recovered__sum"
#     ]
#     Death__sum_after = states_cases.objects.all().aggregate(Sum("Death"))["Death__sum"]

#     date_after = str(states_cases.objects.values("Dated")[0]["Dated"])
#     print(f"DATE AFTER = {date_after}")

#     inc = {
#         "totalcases_inc": confirmed__sum_after,
#         "day_before": date_after,
#         "present_date": date_after,
#         "death_inc": Death__sum_after,
#         "recovered_inc": Recovered__sum_after,
#     }

#     doit = CasesIncrementCheck(
#         confirmed_inc=inc["totalcases_inc"],
#         date_before=inc["day_before"],
#         present_date=inc["present_date"],
#         death_inc=inc["death_inc"],
#         recovered_inc=inc["recovered_inc"],
#         Dated=date_,
#     )
#     doit.save()
#     print(f"DATA UPDATED in CasesIncrementCheck")


# Cases Increment
def cases_increment():
    print("UPDATING INCREMENT DATA")
    CasesIncrementCheck.objects.all().delete()
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

    doit = CasesIncrementCheck(
        confirmed_inc=inc["cases_inc"],
        date_before=inc["day_before"],
        present_date=inc["present_date"],
        death_inc=inc["death_inc"],
        recovered_inc=inc["recovered_inc"],
        Dated=date_,
    )
    doit.save()


def run():
    update_state(url_daily)
    update_district(url_district)
    cases_increment()
    return "SUCCESS"
