import os
from django import forms
from djangolg import fields

# Network display name
NETNAME = "Example Network"

# General contact email
GENERAL_EMAIL = "contact@example.com"
SUPPORT_EMAIL = None
NOC_EMAIL = None
PEERING_EMAIL = None

# Lifetime of session authorisation key in seconds
# Set to 0 for unlimited
LIFETIME = 300

# Maximum number of requests with the same key
# Set to 0 for unlimited
MAX_REQUESTS = 20

# Default salt value for authorisation key generation
SALT = '_signing_salt_'

# Link to Acceptable Use Policy
AUP_LINK = None

# Google reCapture settings
RECAPTCHA_ON = False
RECAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'

# Base template
BASE_TEMPLATE = 'djangolg/base.html'

# Logo Image
LOGO = 'djangolg/img/logo.jpg'

# Small Logo Image
SMALL_LOGO = 'djangolg/img/small_logo.jpg'

# Favicon
FAVICON = 'djangolg/img/favicon.ico'

# Navbar Image
NAV_IMG = None

TEXTFSM_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'textfsm')

# Query methods, and their implementation variables
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

# NOS-dialect-specific command implementations
DIALECTS = {
    'cisco_ios-xe': {
        'index': 0,
        'name': "Cisco IOS-XE",
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

#################################################################
# Don't edit below this line!

try:
    from djangolg.local_settings import *
except Exception:
    pass
