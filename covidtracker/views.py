from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime as dt
import time
from .serializers import DistrictSerializer, StateSerializer
from rest_framework.generics import ListAPIView
# from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import district_cases, states_cases, CasesIncrementCheck, About
from .utils import *

class StateView(ListAPIView):
    queryset = states_cases.objects.all()
    serializer_class = StateSerializer


class DistrictView(ListAPIView):
    queryset = district_cases.objects.all()
    serializer_class = DistrictSerializer


@api_view(["GET"])
def EachStateView(request, s_name):
    queryset = district_cases.objects.all().filter(state_name=s_name)
    serializer = DistrictSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def EachCityCaseView(request, s_name, c_name):
    queryset = district_cases.objects.filter(state_name=s_name, city_name=c_name)
    serializer = DistrictSerializer(queryset, many=True)
    return Response(serializer.data)


date_ = str(dt.now()).split()[0]

# updating if changes made, only for the first user goes to a site

##################################################################################
# Views
# rendering home page
def covid_state(request):
    date_1 = str(dt.now()).split()[0]  # todays date
    # print("DATE1", date_1)
    dated1 = str(district_cases.objects.all().first().Dated)
    query_inc_before = CasesIncrementCheck.objects.all().first()
    dated2 = str(query_inc_before.Dated)
    dated3 = str(states_cases.objects.all().first().Dated)
    # print("district_cases_dated1", dated1)
    # print("CasesIncrementCheck dated2", dated2)
    # print("states_cases dated3", dated3)

    if dated3 != date_1:
        print("UPDATE STATE")
        update_state()
        time.sleep(1)
        if dated2 != date_1:
            print("UPDATE cases inc")
            cases_increment()
    else:
        print("UP TO DATE")

    query_inc_after_updation = CasesIncrementCheck.objects.first()
    confirmed_inc_ = query_inc_after_updation.confirmed_inc
    present_date_ = query_inc_after_updation.present_date
    death_inc_ = query_inc_after_updation.death_inc
    recovered_inc_ = query_inc_after_updation.recovered_inc

    print(f"present _date{present_date_}")
    # sum either after updation or not , above if condition satisfies or not
    confirmed__sum = states_cases.objects.all().aggregate(Sum("confirmed"))
    Active__sum = states_cases.objects.all().aggregate(Sum("Active"))
    Recovered__sum = states_cases.objects.all().aggregate(Sum("Recovered"))
    Death__sum = states_cases.objects.all().aggregate(Sum("Death"))

    intro_modify = About.objects.all()
    context_ = {
        "confirmed": confirmed__sum["confirmed__sum"],
        "Active": Active__sum["Active__sum"],
        "Death": Death__sum["Death__sum"],
        "Recovered": Recovered__sum["Recovered__sum"],
        "district_cases": district_cases.objects.all(),
        "states_cases": states_cases.objects.all().order_by("state_name"),
        "cases_increment": confirmed_inc_,
        "recovered_inc": recovered_inc_,
        "death_inc": death_inc_,
        "present_date": present_date_,
        "title": "INDIA",
        "state": "active",
        "about_intro": About.objects.first(),
        "intro_modifiedDate": intro_modify[0].modified,
    }
    return render(request, "covidtracker/home.html", context_)


# rendering district page
def covid_district(request):
    dated1 = str(district_cases.objects.values("Dated")[0]["Dated"])
    if dated1 != date_:
        update_district()
        print(f"UPDATING DISTRICT CASES on date= {date_}")
    else:
        print("DATA UP TO DATE")
    context_ = {
        "district_cases": district_cases.objects.all().order_by("id"),
        "title": "District",
        "district": "active",
    }
    return render(request, "covidtracker/district.html", context_)


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
