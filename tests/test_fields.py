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
"""Field test classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.test import TestCase

from djangolg import fields, models


class FieldTestCase(TestCase):
    """Test djangolg fields."""

    def test_ip_prefix_field(self):
        """Test IPPrefixField deserialisation."""
        ipv4_prefix = "192.0.2.0/24"
        ipv6_prefix = "2001:db8::/32"
        not_prefix = "A.B.C.D/L"
        field = fields.IPPrefixField()
        assert field.to_python() is None
        assert "{}".format(field.to_python(ipv4_prefix)) == ipv4_prefix
        assert "{}".format(field.to_python(ipv6_prefix)) == ipv6_prefix
        try:
            field.to_python(not_prefix)
        except Exception as e:
            assert isinstance(e, ValidationError)

    def test_ip_address_field(self):
        """Test IPAddressField deserialisation."""
        ipv4_address = "192.0.2.1"
        ipv6_address = "2001:db8::1"
        not_address = "A.B.C.D"
        field = fields.IPAddressField()
        assert field.to_python() is None
        assert "{}".format(field.to_python(ipv4_address)) == ipv4_address
        assert "{}".format(field.to_python(ipv6_address)) == ipv6_address
        try:
            field.to_python(not_address)
        except Exception as e:
            assert isinstance(e, ValidationError)

    def test_router_label(self):
        """Test Router label rendering."""
        class DummyRouterWithLabel(models.Router): # noqa
            """Dummy router subclass for testing."""
            label = "router-label-string"
        class DummyRouterWithoutLabel(models.Router): # noqa
            """Dummy router subclass for testing."""
            @property
            def label(self):
                """Raise error."""
                raise NotImplementedError
        field = fields.RouterChoiceField(queryset=models.Router.objects.all())
        router_with_label = DummyRouterWithLabel(hostname="test-router")
        router_without_label = DummyRouterWithoutLabel(hostname="test-router")
        assert field.label_from_instance(
            router_with_label) == "router-label-string"
        assert field.label_from_instance(
            router_without_label) == "test-router"
