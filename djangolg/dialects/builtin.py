from djangolg.dialects.base import BaseDialect


class CiscoIOSDialect(BaseDialect):
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
