import ipaddress

HOST = 0
PREFIX = 1


class IPPrefix(object):
    def __init__(self, value):
        try:
            obj = ipaddress.ip_address(value)
        except Exception:
            try:
                obj = ipaddress.ip_network(value, strict=False)
            except:
                raise
        if type(obj) in [ ipaddress.IPv4Address, ipaddress.IPv6Address ]:
            self.prefix = None
            self.type = HOST
        elif type(obj) in [ ipaddress.IPv4Network, ipaddress.IPv6Network ]:
            self.prefix = obj.network_address
            self.type = PREFIX
        self.version = obj.version
        self.txt = obj.compressed

    def __str__(self):
        return self.txt

    def __unicode__(self):
        return self.__str__()
