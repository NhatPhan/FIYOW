# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-05 14:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SIAUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('postal_address', models.CharField(max_length=500, null=True)),
                ('residence_country', models.CharField(max_length=200, null=True)),
                ('nationality', models.CharField(max_length=200, null=True)),
                ('dob', models.DateField(null=True, verbose_name='Date of birth')),
                ('language', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
