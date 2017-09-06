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
"""BGP AS Path method class for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django import forms

from djangolg.methods.base import BaseMethod


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
