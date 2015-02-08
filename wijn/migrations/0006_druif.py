# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wijn', '0005_score_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Druif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kleur', models.CharField(max_length=255)),
                ('cp', models.BooleanField(default=True)),
                ('druif', models.CharField(max_length=255)),
                ('appellation', models.ForeignKey(to='wijn.Appellation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
