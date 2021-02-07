from django.db import models


class states_cases(models.Model):
    state_name = models.CharField(max_length=50, unique=True, default="state")
    confirmed = models.IntegerField(blank=True, default=0)
    Death = models.IntegerField(blank=True, default=0)
    Recovered = models.IntegerField(blank=True, default=0)
    Active = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.state_name

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

    def __str__(self):
        return f"{self.state_name}->{self.city_name}"

    def save(self):
        super().save()
