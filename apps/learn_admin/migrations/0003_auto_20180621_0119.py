# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-21 01:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn_admin', '0002_auto_20180620_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='written_on',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recieved_post', to='learn_admin.User'),
        ),
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
