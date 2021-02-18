from rest_framework import routers, serializers, viewsets
from .models import *


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = states_cases
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = district_cases
        fields = "__all__"
