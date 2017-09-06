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
"""Builtin method classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django import forms

from djangolg.methods.base import BaseMethod


class BGPCommunityMethod(BaseMethod):
    """Look up BGP RIB entries by AS_PATH."""

    name = "bgp_community"
    title = "BGP Community"
    new = True
    description = """
    Look up BGP RIB entries with a COMMUNITIES attribute that contains the
    target value. The Community Value field accepts a pair of colon-seperated
    16-bit decimal numbers. Some platforms may also support named "well known"
    community values such as 'no-export', etc. Options are provided to select
    either the IPv4 or the IPv6 address family.
    """
    target_field = forms.CharField(
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': "Community Value",
            'data-toggle': 'tooltip',
            'title': "RFC1997 Community Value"
        }),
    )
    options = ["IPv4", "IPv6"]
    test_target = "65000:65000"
