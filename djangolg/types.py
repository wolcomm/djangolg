from __future__ import print_function
from __future__ import unicode_literals

import ipaddress


class IPPrefix(object):
    HOST = 0
    PREFIX = 1

    def __init__(self, value):
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
        return self.txt

    def __unicode__(self):
        return self.__str__()
