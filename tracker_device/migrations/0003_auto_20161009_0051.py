# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-09 00:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_device', '0002_datapoint'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='tracker_device.TrackerDevice')),
            ],
        ),
        migrations.AlterField(
            model_name='datapoint',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='tracker_device.TrackerDevice'),
        ),
    ]
