# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wijn', '0010_auto_20150821_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='docgdruif',
            name='kleur',
            field=models.CharField(default='?', max_length=255),
            preserve_default=False,
        ),
    ]
