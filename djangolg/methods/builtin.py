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


class BGPASPathMethod(BaseMethod):
    """Look up BGP RIB entries by AS_PATH."""

    name = "bgp_as_path"
    title = "BGP AS Path"
    description = """
    Look up BGP RIB entries with an AS_PATH attribute matching the target
    regular expression. The AS Path Regex field accepts Cisco IOS style regular
    expressions. Options are provided to select either the IPv4 or the IPv6
    address family.
    """
    target_field = forms.CharField(
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': "AS Path Regex",
            'data-toggle': 'tooltip',
            'title': "AS path regular expression"
        }),
    )
    options = ["IPv4", "IPv6"]
    test_target = "_65000_"


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


class PingMethod(BaseMethod):
    """Ping target address."""

    name = "ping"
    title = "Ping"
    description = """
    Send a series of ICMP echo requests to the target IP address, and report
    whether responses were received. Target Address field accepts both IPv4 and
    IPv6 addresses, but not DNS names. The source address of the generated
    requests will default to the address on the first loopback interface of the
    selected router.
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
