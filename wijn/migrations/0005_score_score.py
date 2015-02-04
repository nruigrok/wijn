# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wijn', '0004_score_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
