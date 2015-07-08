# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('plate', models.CharField(max_length=50)),
                ('origin_lat', models.FloatField(blank=True)),
                ('origin_lon', models.FloatField(blank=True)),
                ('destination_lat', models.FloatField(blank=True)),
                ('destination_lon', models.FloatField(blank=True)),
                ('emergency', models.CharField(max_length=50, blank=True)),
                ('battery_life', models.PositiveSmallIntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='DropPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('altitude', models.FloatField()),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hangar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('altitude', models.FloatField()),
                ('radius', models.FloatField()),
                ('is_available', models.BooleanField(default=True)),
                ('drone', models.ForeignKey(to='faed_management.Drone')),
                ('drop_points', models.ManyToManyField(to='faed_management.DropPoint')),
            ],
        ),
        migrations.CreateModel(
            name='MeteoStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('altitude', models.FloatField()),
                ('is_available', models.BooleanField(default=True)),
                ('temperature', models.FloatField()),
                ('wind_speed', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='StyleURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('href', models.URLField()),
                ('scale', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='meteostation',
            name='style_url',
            field=models.ForeignKey(to='faed_management.StyleURL'),
        ),
        migrations.AddField(
            model_name='hangar',
            name='style_url',
            field=models.ForeignKey(to='faed_management.StyleURL'),
        ),
        migrations.AddField(
            model_name='droppoint',
            name='style_url',
            field=models.ForeignKey(to='faed_management.StyleURL'),
        ),
        migrations.AddField(
            model_name='drone',
            name='style_url',
            field=models.ForeignKey(to='faed_management.StyleURL'),
        ),
    ]
