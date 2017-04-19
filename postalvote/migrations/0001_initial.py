# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import useful_inkleby.useful_django.models.mixins


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Council',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch_time', models.DateTimeField(null=True, editable=False, blank=True)),
                ('batch_id', models.IntegerField(null=True, editable=False, blank=True)),
                ('name', models.CharField(default=b'', max_length=255, blank=True)),
                ('website', models.CharField(default=b'', max_length=255, blank=True)),
                ('postcode', models.CharField(default=b'', max_length=9, blank=True)),
                ('lad13cd', models.CharField(default=b'', max_length=13, blank=True)),
                ('address', models.TextField(default=0)),
                ('email', models.CharField(default=b'', max_length=255, blank=True)),
                ('phone', models.CharField(default=b'', max_length=255, blank=True)),
                ('forms_completed', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, useful_inkleby.useful_django.models.mixins.StockModelHelpers),
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch_time', models.DateTimeField(null=True, editable=False, blank=True)),
                ('batch_id', models.IntegerField(null=True, editable=False, blank=True)),
                ('name', models.CharField(default=b'', max_length=255, blank=True)),
                ('date', models.DateField()),
                ('cut_off_date', models.DateField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, useful_inkleby.useful_django.models.mixins.StockModelHelpers),
        ),
        migrations.CreateModel(
            name='Postcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch_time', models.DateTimeField(null=True, editable=False, blank=True)),
                ('batch_id', models.IntegerField(null=True, editable=False, blank=True)),
                ('postcode', models.CharField(db_index=True, max_length=7, blank=True)),
                ('multi_council', models.IntegerField(default=0)),
                ('council', models.ForeignKey(related_name='postcode_refs', blank=True, to='postalvote.Council', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, useful_inkleby.useful_django.models.mixins.StockModelHelpers),
        ),
    ]
