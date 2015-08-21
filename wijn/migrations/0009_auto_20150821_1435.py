# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wijn', '0008_docg'),
    ]

    operations = [
        migrations.CreateModel(
            name='DOCGDruif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('land', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('i', models.IntegerField()),
                ('druif', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='docg',
            name='druif1',
        ),
        migrations.RemoveField(
            model_name='docg',
            name='druif2',
        ),
        migrations.RemoveField(
            model_name='docg',
            name='druif3',
        ),
        migrations.RemoveField(
            model_name='docg',
            name='druif4',
        ),
        migrations.AddField(
            model_name='streekdruif',
            name='i',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
