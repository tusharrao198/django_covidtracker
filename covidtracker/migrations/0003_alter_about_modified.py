# Generated by Django 3.2.5 on 2021-07-15 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidtracker', '0002_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='modified',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]