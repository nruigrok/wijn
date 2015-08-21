# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wijn', '0009_auto_20150821_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streekdruif',
            name='region',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
