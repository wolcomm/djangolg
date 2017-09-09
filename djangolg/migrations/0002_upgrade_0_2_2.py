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
"""Upgrade migration definition for djangolg for version 0.2.2."""

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration definition."""

    dependencies = [
        ('djangolg', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='sitecode',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='event',
            field=models.IntegerField(choices=[(0, 'Session Started'),
                                               (1, 'Query Authorised'),
                                               (2, 'Query Rejected'),
                                               (3, 'Invalid Query'),
                                               (4, 'Query Execution Failed'),
                                               (5, 'Unhandled Error')]),
        ),
        migrations.AlterField(
            model_name='log',
            name='key',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='src_host',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='router',
            name='dialect',
            field=models.CharField(choices=[('ios', 'Cisco IOS')],
                                   max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='router',
            name='hostname',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
