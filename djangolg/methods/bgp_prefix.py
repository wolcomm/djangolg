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
"""BGP Prefix method class for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django import forms

from djangolg import fields
from djangolg.methods.base import BaseMethod


class BGPPrefixMethod(BaseMethod):
    """Look up BGP RIB entries for the target IP prefix."""

    name = "bgp_prefix"
    title = "BGP Prefix"
    description = """
    Look up BGP RIB entries for the target IP prefix. The prefix field accepts
    both IPv4 and IPv6 address families. Options are provided to search for all
    exact-match paths, the BGP bestpath only, or all longer-match paths.
    """
    target_field = fields.IPPrefixField(
        required=True,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': "Prefix",
            'data-toggle': 'tooltip',
            'title': "IP address or prefix"
        }),
        label='Prefix'
    )
    options = ["All paths", "Bestpath Only", "Longer Prefixes"]
    test_target = fields.IPPrefixField().to_python(value="2001:db8::/32")
