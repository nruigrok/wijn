# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wijn', '0006_druif'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreekDruif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('land', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('kleur', models.CharField(max_length=255)),
                ('druif', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StreekWijn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('land', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('subregion', models.CharField(max_length=255, null=True)),
                ('gemeente', models.CharField(max_length=255, null=True)),
                ('appellation', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
