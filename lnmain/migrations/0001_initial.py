# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-11 00:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ch_Addresses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt100_address', models.CharField(max_length=6)),
                ('overflow_address', models.CharField(max_length=6)),
                ('valve_address', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='LNFillCong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_id', models.CommaSeparatedIntegerField(max_length=20, unique=True)),
                ('ch_type', models.IntegerField(choices=[(0, 'Manifold'), (1, 'Vent'), (2, 'Detector')], default=2)),
                ('ch_name', models.CharField(max_length=30)),
                ('ch_enable', models.IntegerField(choices=[(0, 'Disable'), (1, 'Enable')])),
                ('ch_addresses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lnmain.Ch_Addresses')),
            ],
        ),
    ]
