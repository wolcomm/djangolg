DIALECTS = {
    'ios': {
        'index': 0,
        'name': "Cisco IOS",
        'cmds': {
            'bgp_prefix': {
                'options': [
                    {'label': "All paths",
                     'cmd': lambda target: "show bgp ipv%s unicast %s" % (target.version, str(target))},
                    {'label': "Bestpath Only",
                     'cmd': lambda target: "show bgp ipv%s unicast %s bestpath" % (target.version, str(target))},
                    {'label': "Longer Prefixes",
                     'cmd': lambda target: "show bgp ipv%s unicast %s longer-prefixes | begin Network" % (target.version, str(target)),
                     'template': 'bgp_prefix_longer.textfsm'},
                ]
            },
            'bgp_as_path': {
                'options': [
                    {'label': "IPv4",
                     'cmd': lambda target: "show bgp ipv4 unicast quote-regexp \"%s\" | begin Network" % str(target)},
                    {'label': "IPv6",
                     'cmd': lambda target: "show bgp ipv6 unicast quote-regexp \"%s\" | begin Network" % str(target)},
                ]
            },
            'bgp_community': {
                'options': [
                    {'label': "IPv4",
                     'cmd': lambda target: "show bgp ipv4 unicast community %s | begin Network" % str(target)},
                    {'label': "IPv6",
                     'cmd': lambda target: "show bgp ipv6 unicast community %s | begin Network" % str(target)},
                ]
            },
            'ping': {
                'cmd': lambda target: "ping %s source Loopback0" % (str(target))
            },
            'trace_route': {
                'cmd': lambda target: "traceroute %s" % (str(target))
            }
        }
    }
}


def dialects():
    D = sorted(DIALECTS.items(), key=lambda d: d[1]['index'])
    return [d[0] for d in D]


def dialect_choices():
    return [(d, Dialect(d).name) for d in dialects()]


class Dialect(object):
    def __init__(self, dialect):
        if dialect in dialects():
            self._dialect = DIALECTS[dialect]
        else:
            raise ValueError
        self._str = dialect

    @property
    def index(self):
        return self._dialect['index']

    @property
    def name(self):
        return self._dialect['name']

    @property
    def cmds(self):
        return self._dialect['cmds']

    def __str__(self):
        return self._str
