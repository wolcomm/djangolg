from django import forms
from djangolg import fields

METHODS = {
    'bgp_prefix': {
        'index': 0,
        'name': 'bgp_prefix',
        'title': "BGP Prefix",
        'description': """
        Look up BGP RIB entries for the target IP prefix.
        The prefix field accepts both IPv4 and IPv6 address families.
        Options are provided to search for all exact-match paths, the BGP bestpath only, or all longer-match paths.
        """,
        'target': fields.IPPrefixField(
            required=True,
            widget=forms.TextInput({
                'class': 'form-control',
                'placeholder': "Prefix",
                'data-toggle': 'tooltip',
                'title': "IP address or prefix"
            }),
            label='Prefix'
        ),
        'options': [
            { 'label': "All paths", 'cmd': lambda target: "show bgp ipv%s unicast %s" % (target.version, str(target)) },
            { 'label': "Bestpath Only", 'cmd': lambda target: "show bgp ipv%s unicast %s bestpath" % (target.version, str(target)) },
            { 'label': "Longer Prefixes", 'cmd': lambda target: "show bgp ipv%s unicast %s longer-prefixes | begin Network" % (target.version, str(target)) },
        ],
        'cmd': lambda target: "show bgp ipv%s unicast %s" % (target.version, str(target))
    },
    'bgp_as_path': {
        'index': 1,
        'name': 'bgp_as_path',
        'title': "BGP AS Path",
        'description': """
        Look up BGP RIB entries with an AS_PATH attribute matching the target regular expression.
        The AS Path Regex field accepts Cisco IOS style regular expressions.
        Options are provided to select either the IPv4 or the IPv6 address family.
        """,
        'target': forms.CharField(
            widget=forms.TextInput({
                'class': 'form-control',
                'placeholder': "AS Path Regex",
                'data-toggle': 'tooltip',
                'title': "AS path regular expression"
            }),
        ),
        'options': [
            { 'label': "IPv4", 'cmd': lambda target: "show bgp ipv4 unicast quote-regexp \"%s\" | begin Network" % str(target) },
            { 'label': "IPv6", 'cmd': lambda target: "show bgp ipv6 unicast quote-regexp \"%s\" | begin Network" % str(target) },
        ],
        'cmd': lambda target: "show bgp %s unicast regex %s" % ('ipv4', str(target))
    },
    'bgp_community': {
        'index': 2,
        'name': 'bgp_community',
        'title': "BGP Community",
        'new': True,
        'description': """
        Look up BGP RIB entries with a COMMUNITIES attribute that contains the target value.
        The Community Value field accepts a pair of colon-seperated 16-bit decimal numbers.
        Some platforms may also support named "well known" community values such as 'no-export', etc.
        Options are provided to select either the IPv4 or the IPv6 address family.
        """,
        'target': forms.CharField(
            widget=forms.TextInput({
                'class': 'form-control',
                'placeholder': "Community Value",
                'data-toggle': 'tooltip',
                'title': "RFC1997 Community Value"
            }),
        ),
        'options': [
            { 'label': "IPv4", 'cmd': lambda target: "show bgp ipv4 unicast community %s | begin Network" % str(target) },
            { 'label': "IPv6", 'cmd': lambda target: "show bgp ipv6 unicast community %s | begin Network" % str(target) },
        ],
        'cmd': lambda target: "show bgp %s unicast community %s" % ('ipv4', str(target))
    },
    'ping': {
        'index': 3,
        'name': 'ping',
        'title': "Ping",
        'description': """
        Send a series of ICMP echo requests to the target IP address, and report whether responses were received.
        Target Address field accepts both IPv4 and IPv6 addresses, but not DNS names.
        The source address of the generated requests will default to the address on the first loopback interface of the
        selected router.
        """,
        'target': fields.IPAddressField(
            widget=forms.TextInput({
                'class': 'form-control',
                'placeholder': "Target Address",
                'data-toggle': 'tooltip',
                'title': "Target IP address"
            }),
        ),
        'cmd': lambda target: "ping %s source Loopback0" % (str(target))
    },
    'trace_route': {
        'index': 4,
        'name': 'trace_route',
        'title': 'Traceroute',
        'description': """
        Perform a traceroute from the selected router to the target IP address.
        Target Address field accepts both IPv4 and IPv6 addresses, but not DNS names.
        """,
        'target': fields.IPAddressField(
            widget=forms.TextInput({
                'class': 'form-control',
                'placeholder': "Target Address",
                'data-toggle': 'tooltip',
                'title': "Target IP address"
            }),
        ),
        'cmd': lambda target: "traceroute %s" % (str(target))
    }
}


def methods():
    M = sorted(METHODS.items(), key=lambda m: m[1]['index'])
    return [m[0] for m in M]


class Method(object):
    def __init__(self, method):
        if method in methods():
            self.method = METHODS[method]
        else:
            raise KeyError
        self._dialect = None

    @property
    def dialect(self):
        return self._dialect

    @dialect.setter
    def dialect(self, dialect=None):
        if self.name in dialect.cmds:
            self._dialect = dialect
        else:
            raise NotImplementedError

    @property
    def name(self):
        return self.method['name']

    @property
    def title(self):
        return self.method['title']

    @property
    def description(self):
        return self.method['description']

    @property
    def target(self):
        return self.method['target']

    @property
    def new(self):
        try:
            return self.method['new']
        except KeyError:
            return False

    @property
    def options(self):
        if self.dialect:
            if 'options' in self.dialect.cmds[self.name]:
                return self.dialect.cmds[self.name]['options']
        else:
            if 'options' in self.method:
                return self.method['options']
        return []

    @property
    def option_choices(self):
        return ( (self.options.index(option), option['label']) for option in self.options )

    @property
    def cmd(self):
        if self.dialect:
            return self.dialect.cmds[self.name]['cmd']
        else:
            return self.method['cmd']

    @property
    def template(self):
        if self.dialect:
            return self.dialect.cmds[self.name]['template']
        else:
            return self.method['template']
