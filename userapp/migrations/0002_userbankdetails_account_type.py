# Generated by Django 3.2.1 on 2021-05-28 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbankdetails',
            name='account_type',
            field=models.CharField(choices=[('cur', 'Current'), ('sal', 'Salary'), ('sav', 'Savings')], default=None, max_length=30),
            preserve_default=False,
        ),
    ]