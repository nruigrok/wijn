# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wijn', '0007_streekdruif_streekwijn'),
    ]

    operations = [
        migrations.CreateModel(
            name='DOCG',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('land', models.CharField(max_length=255)),
                ('regio', models.CharField(max_length=255)),
                ('subregio', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
                ('isDOCG', models.BooleanField()),
                ('druif1', models.CharField(max_length=255, null=True)),
                ('druif2', models.CharField(max_length=255, null=True)),
                ('druif3', models.CharField(max_length=255, null=True)),
                ('druif4', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
