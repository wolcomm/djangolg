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
"""Traceroute method class for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django import forms

from djangolg import fields
from djangolg.methods.base import BaseMethod


class TracerouteMethod(BaseMethod):
    """Traceroute to target address."""

    name = "trace_route"
    title = "Traceroute"
    description = """
    Perform a traceroute from the selected router to the target IP address.
    Target Address field accepts both IPv4 and IPv6 addresses, but not DNS
    names.
    """
    target_field = fields.IPAddressField(
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': "Target Address",
            'data-toggle': 'tooltip',
            'title': "Target IP address"
        }),
    )
    test_target = fields.IPAddressField().to_python(value="2001:db8::1")
