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
"""Method test classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.test import TestCase

from djangolg import dialects, methods
from djangolg.methods.base import BaseMethod


class MethodTestCase(TestCase):
    """Test djangolg methods."""

    def test_available_methods(self):
        """Test available_methods helper."""
        methods_map = methods.available_methods("map")
        methods_list = methods.available_methods("list")
        assert isinstance(methods_map, dict)
        assert isinstance(methods_list, list)
        try:
            methods.available_methods("wrong")
        except Exception as e:
            assert isinstance(e, ValueError)
            assert "{}".format(e) == "invalid output type: wrong"

    def test_get_method(self):
        """Test get_method helper."""
        for method_name in methods.available_methods("list"):
            method = methods.get_method(name=method_name)
            assert isinstance(method, BaseMethod)
        try:
            methods.get_method()
        except Exception as e:
            assert isinstance(e, methods.MethodNotFound)
        try:
            methods.get_method(name=dict())
        except Exception as e:
            assert isinstance(e, methods.LookingGlassMethodError)

    def test_method_init_failure(self):
        """Test method initiation failure."""
        try:
            BaseMethod(dialect="string")
        except Exception as e:
            assert isinstance(e, TypeError)

    def test_method_dialect_functions(self):
        """Test method dialect getter and setter and other methods."""
        for method_name in methods.available_methods(output="list"):
            method = methods.get_method(name=method_name)
            assert method.dialect is None
            try:
                method.dialect = "wrong_type"
            except Exception as e:
                assert isinstance(e, TypeError)
            for dialect_name in dialects.available_dialects(output="list"):
                dialect = dialects.get_dialect(dialect_name)
                method.dialect = dialect
                assert method.dialect is dialect
                if method.options:
                    for index, option in method.option_choices():
                        assert method.get_command(target=method.test_target,
                                                  option_index=index)
                else:
                    assert method.get_command(target=method.test_target)
