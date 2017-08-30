# -*- coding: utf-8 -*-
# Copyright 2017 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Initial migration definition for djangolg."""

from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration definition."""

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('type', models.IntegerField(choices=[(0, 'Password'),
                                                      (1, 'Public Key')])),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('pubkey', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sitecode', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('event', models.IntegerField(choices=[(0, 'Session Started'),
                                                       (1, 'Query Authorised'),
                                                       (2, 'Query Rejected'),
                                                       (3, 'Invalid Query')])),
                ('src_host', models.CharField(max_length=20)),
                ('method_name', models.CharField(max_length=20, null=True)),
                ('target', models.CharField(max_length=20, null=True)),
                ('key', models.CharField(max_length=40, null=True)),
                ('error', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Router',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=20, unique=True)),
                ('dialect', models.CharField(choices=[(b'cisco_ios-xe',
                                                       b'Cisco IOS-XE')],
                                             max_length=20, null=True)),
                ('credentials', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL,
                    to='djangolg.Credential')),
                ('location', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL,
                    to='djangolg.Location')),
            ],
        ),
        migrations.AddField(
            model_name='log',
            name='router',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL,
                to='djangolg.Router'),
        ),
    ]
