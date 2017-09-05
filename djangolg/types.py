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
"""Custom type classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

import ipaddress


class IPPrefix(object):
    """Generic IP prefix class."""

    HOST = 0
    PREFIX = 1

    def __init__(self, value):
        """Initialise new IPPrefix instance."""
        try:
            obj = ipaddress.ip_address(value)
        except Exception:
            try:
                obj = ipaddress.ip_network(value, strict=False)
            except Exception:
                raise
        if type(obj) in [ipaddress.IPv4Address, ipaddress.IPv6Address]:
            self.prefix = None
            self.type = self.HOST
        elif type(obj) in [ipaddress.IPv4Network, ipaddress.IPv6Network]:
            self.prefix = obj.network_address
            self.type = self.PREFIX
        self.version = obj.version
        self.txt = obj.compressed

    def __str__(self):
        """Return string representation."""
        return self.txt

    def __unicode__(self):
        """Return string representation."""
        return self.__str__()  # pragma: no cover
