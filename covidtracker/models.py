from django.db import models
from datetime import datetime as dt

date_ = str(dt.now()).split()[0]


class states_cases(models.Model):
    state_name = models.CharField(max_length=50, unique=True, default="state")
    confirmed = models.IntegerField(blank=True, default=0)
    Death = models.IntegerField(blank=True, default=0)
    Recovered = models.IntegerField(blank=True, default=0)
    Active = models.IntegerField(blank=True, default=0)
    Dated = models.TextField(blank=False, null=False, default=date_)

    def __str__(self):
        return f"{self.state_name}"

    def save(self):
        super().save()


class district_cases(models.Model):
    city_name = models.CharField(max_length=100, default="city")
    state_name = models.CharField(
        max_length=50, default="state", null=False, blank=False
    )
    confirmed = models.IntegerField(blank=True, default=0)
    Death = models.IntegerField(blank=True, default=0)
    Recovered = models.IntegerField(blank=True, default=0)
    Active = models.IntegerField(blank=True, default=0)
    Dated = models.TextField(blank=False, null=False, default=date_)

    def __str__(self):
        return f"{self.state_name}->{self.city_name}->{self.Dated}"

    def save(self):
        super().save()


class CasesIncrementCheck(models.Model):
    confirmed_inc = models.IntegerField(blank=False, default=0, null=False)
    date_before = models.TextField(blank=False, default=0, null=False)
    present_date = models.TextField(blank=False, default=0, null=False)
    death_inc = models.IntegerField(blank=False, default=0, null=False)
    recovered_inc = models.IntegerField(blank=False, default=0, null=False)
    Dated = models.TextField(blank=False, null=False, default=date_)

    def __str__(self):
        return f"{self.Dated}"

    def save(self):
        super().save()
