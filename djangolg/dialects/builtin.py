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
"""Builtin dialect classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from djangolg.dialects.base import BaseDialect


class CiscoIOSDialect(BaseDialect):
    """Cisco IOS Classic/XE dialect."""

    name = "ios"
    description = "Cisco IOS"
    commands = {
        'bgp_prefix': {
            "All paths": lambda target:
                "show bgp ipv{0} unicast {1}"
                .format(target.version, str(target)),
            "Bestpath Only": lambda target:
                "show bgp ipv{0} unicast {1} bestpath"
                .format(target.version, str(target)),
            "Longer Prefixes": lambda target:
                "show bgp ipv{0} unicast {1} longer-prefixes | begin Network"
                .format(target.version, str(target)),
        },
        'bgp_as_path': {
            "IPv4": lambda target:
                "show bgp ipv4 unicast quote-regexp \"{0}\" | begin Network"
                .format(str(target)),
            "IPv6": lambda target:
                "show bgp ipv6 unicast quote-regexp \"{0}\" | begin Network"
                .format(str(target)),
        },
        'bgp_community': {
            "IPv4": lambda target:
                "show bgp ipv4 unicast community {0} | begin Network"
                .format(str(target)),
            "IPv6": lambda target:
                "show bgp ipv6 unicast community {0} | begin Network"
                .format(str(target)),
        },
        'ping': lambda target:
            "ping {0} source Loopback0".format(str(target)),
        'trace_route': lambda target:
            "traceroute {0}".format(str(target)),
    }
