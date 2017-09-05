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
"""Management command test classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils.six import StringIO


class LGManagementTestCase(TestCase):
    """Test djangolg management commands."""

    commands = [
        {'obj': 'credentials', 'opts': {
            'name': 'test-credentials', 'type': 0,
            'username': 'test', 'password': 'test'
        }},
        {'obj': 'locations', 'opts': {
            'name': 'test-location', 'sitecode': 'test'
        }},
        {'obj': 'routers', 'opts': {
            'hostname': 'test-router', 'dialect': 'ios',
            'location': 1, 'credentials': 1
        }}
    ]

    def test_lg_commands(self):  # noqa
        """Test the lg management command."""
        # list objects - before creating anything
        for obj in [command['obj'] for command in self.commands]:
            out = StringIO()
            args = ('list', obj)
            call_command('lg', *args, stdout=out)
            expect = "No {} configured".format(obj)
            assert expect in out.getvalue()
        # add objects
        for command in self.commands:
            out = StringIO()
            args = ('add', command['obj'])
            opts = command['opts']
            call_command('lg', *args, stdout=out, **opts)
            expect = "index: 1"
            assert expect in out.getvalue()
        # list objects
        for obj in [command['obj'] for command in self.commands]:
            out = StringIO()
            args = ('list', obj)
            call_command('lg', *args, stdout=out)
            expect = "Configured {}".format(obj.capitalize())
            assert expect in out.getvalue()
        # modify objects
        for command in self.commands:
            args = ('modify', command['obj'])
            for opt in command['opts']:
                out = StringIO()
                opts = {"index": 1, opt: command['opts'][opt]}
                call_command('lg', *args, stdout=out, **opts)
                expect = "index: 1"
                assert expect in out.getvalue()
        # show created objects
        for command in self.commands:
            out = StringIO()
            args = ('show', command['obj'])
            call_command('lg', *args, index=1, stdout=out)
            expect = "index: 1"
            assert expect in out.getvalue()
        # delete objects
        for obj in [command['obj'] for command in self.commands]:
            out = StringIO()
            args = ('delete', obj)
            call_command('lg', *args, index=1, stdout=out)
        # show deleted objects
        for command in self.commands:
            out = StringIO()
            args = ('show', command['obj'])
            try:
                call_command('lg', *args, index=1, stdout=out)
            except Exception as e:
                assert isinstance(e, CommandError)
