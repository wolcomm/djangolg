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

from djangolg import dialects, methods, models
from djangolg.lg import LookingGlass

from napalm_base import NetworkDriver

from tests.lg import DummyLookingGlass


class LGTestCase(TestCase):
    """Test djangolg lg class."""

    def test_init_lg(self):
        """Test LG class instantiation."""
        credentials = models.Credential.objects.create(
            name="test-credentials", type=models.Credential.CRED_TYPE_PASSWD,
            username="test", password="test")
        for dialect_name in dialects.available_dialects(output="list"):
            hostname = "{}-router".format(dialect_name)
            router = models.Router.objects.create(hostname=hostname,
                                                  credentials=credentials,
                                                  dialect=dialect_name)
            lg = LookingGlass(router=router)
            assert isinstance(lg.device, NetworkDriver)

    def test_init_lg_failure(self):
        """Test LG class instantiation failure."""
        try:
            LookingGlass()
        except Exception as e:
            assert isinstance(e, ValueError)

    def test_lg_execution(self):
        """Test dummy LG class."""
        credentials = models.Credential.objects.create(
            name="test-credentials", type=models.Credential.CRED_TYPE_PASSWD,
            username="test", password="test")
        available_methods = methods.available_methods(output="list")
        for dialect_name in dialects.available_dialects(output="list"):
            hostname = "{}-router".format(dialect_name)
            router = models.Router.objects.create(hostname=hostname,
                                                  credentials=credentials,
                                                  dialect=dialect_name)
            with DummyLookingGlass(router=router) as lg:
                for method_name in available_methods:
                    method = methods.get_method(name=method_name)
                    method.dialect = dialects.get_dialect(router.dialect)
                    if method.options:
                        for index, option in method.option_choices():
                            expect = "{0}: {1}".format(
                                router.hostname,
                                method.get_command(
                                    target=method.test_target,
                                    option_index=index
                                )
                            )
                            output = lg.execute(
                                method=method,
                                target=method.test_target,
                                option_index=index
                            )
                            assert output['raw'] == expect
                    else:
                        expect = "{0}: {1}".format(
                            router.hostname,
                            method.get_command(target=method.test_target)
                        )
                        output = lg.execute(method=method,
                                            target=method.test_target)
                        assert output['raw'] == expect
