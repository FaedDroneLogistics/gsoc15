# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faed_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='destination_lat',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='drone',
            name='destination_lon',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='drone',
            name='emergency',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='drone',
            name='origin_lat',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='drone',
            name='origin_lon',
            field=models.FloatField(null=True),
        ),
    ]
