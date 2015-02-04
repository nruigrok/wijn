# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wijn', '0003_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 4, 13, 32, 49, 586910, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
