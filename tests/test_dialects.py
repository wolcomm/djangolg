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
"""Dialect test classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.test import TestCase

from djangolg import dialects
from djangolg.dialects.base import BaseDialect


class DialectTestCase(TestCase):
    """Test djangolg dialects."""

    def test_available_dialects(self):
        """Test available_dialects helper."""
        dialects_map = dialects.available_dialects("map")
        dialects_choices = dialects.available_dialects("choices")
        dialects_list = dialects.available_dialects("list")
        assert isinstance(dialects_map, dict)
        assert isinstance(dialects_choices, list)
        for choice in dialects_choices:
            assert isinstance(choice, tuple)
        assert isinstance(dialects_list, list)
        try:
            dialects.available_dialects("wrong")
        except Exception as e:
            assert isinstance(e, ValueError)
            assert "{}".format(e) == "invalid output type: wrong"

    def test_get_dialect(self):
        """Test get_dialect helper."""
        for dialect_name in dialects.available_dialects("list"):
            dialect = dialects.get_dialect(name=dialect_name)
            assert isinstance(dialect, BaseDialect)
            try:
                dialect.get_command_syntax()
            except Exception as e:
                assert isinstance(e, ValueError)

    def test_bad_dialect_definitions(self):
        """Test error handling for bad dialect definitions."""
        try:
            BaseDialect()
        except Exception as e:
            assert isinstance(e, ValueError)
