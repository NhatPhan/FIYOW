# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-07 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_auto_20161007_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attractionticket',
            name='end_date',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='attractionticket',
            name='start_date',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
