from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime as dt

from django.db.models.fields import DateTimeField

date_ = str(dt.now()).split()[0]


# As a common base model for models which there is no primary key set, inherit this class
class CommonBaseModel(models.Model):
    # if not defining primary set it to AutoField or BigAutoField
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class states_cases(CommonBaseModel):
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


class district_cases(CommonBaseModel):
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


class About(models.Model):
    intro = RichTextField(blank=True, null=True)
    modified = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    def __str__(self):
        return self.intro

    def save(self):
        super().save()
