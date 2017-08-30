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
"""Custom django field definitions."""

from __future__ import print_function
from __future__ import unicode_literals

import ipaddress

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from djangolg import types


# TODO: Provide options to disallow reserved/multicast addresses
class IPPrefixField(forms.CharField):
    """IP Prefix field."""

    def to_python(self, value):
        """Deserialise to python type."""
        if not value:
            return None
        try:
            prefix = types.IPPrefix(value)
        except Exception:
            raise ValidationError(
                _('%(value)s is not a valid ip prefix'),
                params={'value': value}
            )
        return prefix


class IPAddressField(forms.CharField):
    """IP Address field."""

    def to_python(self, value):
        """Deserialise to python type."""
        if not value:
            return None
        try:
            address = ipaddress.ip_address(value)
        except Exception:
            raise ValidationError(
                _('%(value)s is not a valid ip address'),
                params={'value': value}
            )
        return address


class RouterChoiceField(forms.ModelChoiceField):
    """Router selection field."""

    def label_from_instance(self, obj):
        """Render field label."""
        try:
            label = obj.label
        except NotImplementedError:
            label = str(obj)
        return label
