# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-17 20:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import mirrors.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CheckLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=255)),
                ('source_ip', models.GenericIPAddressField(unique=True, unpack_ipv4=True, verbose_name='source IP')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('created', models.DateTimeField(editable=False)),
            ],
            options={
                'ordering': ('hostname', 'source_ip'),
            },
        ),
        migrations.CreateModel(
            name='Mirror',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('tier', models.SmallIntegerField(choices=[(0, 'Tier 0'), (1, 'Tier 1'), (2, 'Tier 2'), (-1, 'Untiered')], default=2)),
                ('admin_email', models.EmailField(blank=True, max_length=255)),
                ('alternate_email', models.EmailField(blank=True, max_length=255)),
                ('public', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('isos', models.BooleanField(default=True, verbose_name='ISOs')),
                ('rsync_user', models.CharField(blank=True, default='', max_length=50)),
                ('rsync_password', models.CharField(blank=True, default='', max_length=50)),
                ('bug', models.PositiveIntegerField(blank=True, null=True, verbose_name='Flyspray bug')),
                ('notes', models.TextField(blank=True)),
                ('created', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('upstream', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mirrors.Mirror')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='MirrorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_time', models.DateTimeField(db_index=True)),
                ('last_sync', models.DateTimeField(null=True)),
                ('duration', models.FloatField(null=True)),
                ('is_success', models.BooleanField(default=True)),
                ('error', models.TextField(blank=True, default='')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='mirrors.CheckLocation')),
            ],
            options={
                'get_latest_by': 'check_time',
                'verbose_name': 'mirror check log',
            },
        ),
        migrations.CreateModel(
            name='MirrorProtocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol', models.CharField(max_length=10, unique=True)),
                ('is_download', models.BooleanField(default=True, help_text='Is protocol useful for end-users, e.g. HTTP')),
                ('default', models.BooleanField(default=True, help_text='Included by default when building mirror list?')),
                ('created', models.DateTimeField(editable=False)),
            ],
            options={
                'ordering': ('protocol',),
            },
        ),
        migrations.CreateModel(
            name='MirrorRsync',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', mirrors.fields.IPNetworkField(max_length=44, verbose_name='IP')),
                ('created', models.DateTimeField(editable=False)),
                ('mirror', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rsync_ips', to='mirrors.Mirror')),
            ],
            options={
                'ordering': ('ip',),
                'verbose_name': 'mirror rsync IP',
            },
        ),
        migrations.CreateModel(
            name='MirrorUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255, unique=True, verbose_name='URL')),
                ('country', django_countries.fields.CountryField(blank=True, db_index=True, max_length=2)),
                ('has_ipv4', models.BooleanField(default=True, editable=False, verbose_name='IPv4 capable')),
                ('has_ipv6', models.BooleanField(default=False, editable=False, verbose_name='IPv6 capable')),
                ('created', models.DateTimeField(editable=False)),
                ('active', models.BooleanField(default=True)),
                ('mirror', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='mirrors.Mirror')),
                ('protocol', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='urls', to='mirrors.MirrorProtocol')),
                ('bandwidth', models.FloatField(blank=True, null=True, verbose_name='bandwidth (mbits)')),
            ],
            options={
                'verbose_name': 'mirror URL',
            },
        ),
        migrations.AddField(
            model_name='mirrorlog',
            name='url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='mirrors.MirrorUrl'),
        ),
    ]