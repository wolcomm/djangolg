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
"""Exception test classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.test import TestCase

from djangolg import exceptions


class ExceptionTestCase(TestCase):
    """Test djangolg custom exceptions."""

    def test_type_check_helper(self):
        """Test check_type helper."""
        class DummyClass(object): #noqa
            """A dummy class for testing purposes."""
            pass
        class DummySubClass(DummyClass): #noqa
            """A dummy subclass for testing purposes."""
            pass
        # these checks should pass
        pass_dict = {
            (0,): tuple, 0: int,
            DummyClass: type, DummySubClass(): DummyClass,
        }
        for instance, classinfo in pass_dict.items():
            exceptions.check_type(instance=instance, classinfo=classinfo)
        # these should fail
        fail_dict = {
            (0,): list, 0: str,
            DummySubClass: DummyClass, DummyClass(): DummySubClass,
        }
        for instance, classinfo in fail_dict.items():
            try:
                exceptions.check_type(instance=instance, classinfo=classinfo)
            except Exception as e:
                assert isinstance(e, exceptions.TypeCheckError)

    def test_default_error_message(self):
        """Test default_error_message helper."""
        test_string = "default message string"
        exc = exceptions.LookingGlassError(test_string)
        assert exc.log_error == "{0}: {1}".format(exc.__class__.__name__,
                                                  test_string)
