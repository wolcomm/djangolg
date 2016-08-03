from django import forms
from djangolg import fields

# Network display name
NETNAME = "Default Network"

# General contact email
GENERAL_EMAIL = "contact@example.com"

# Lifetime of session authorisation key in seconds
# Set to 0 for unlimited
LIFETIME = 300

# Maximum number of requests with the same key
# Set to 0 for unlimited
MAX_REQUESTS = 20

# TODO: Provide dialect-specific cmd syntax
# Query methods, and their implementation variables
METHODS = {
    'bgp_prefix': {
        'index': 0,
        'name': 'bgp_prefix',
        'title': "BGP Prefix Query",
        'target': fields.IPPrefixField(
            required=True,
            widget=forms.TextInput(
                {'class': 'form-control'}
            ),
            label_suffix='',
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
        'title': "BGP AS Path Query",
        'target': forms.CharField(
            required=True,
            widget=forms.TextInput(
                {'class': 'form-control'}
            ),
            label_suffix='',
            label='AS Path Regex'
        ),
        'options': [
            { 'label': "IPv4", 'cmd': lambda target: "show bgp ipv4 unicast quote-regexp \"%s\" | begin Network" % str(target) },
            { 'label': "IPv6", 'cmd': lambda target: "show bgp ipv6 unicast quote-regexp \"%s\" | begin Network" % str(target) },
        ],
        'cmd': lambda target: "show bgp %s unicast regex %s" % ('ipv4', str(target))
    },
    'ping': {
        'index': 2,
        'name': 'ping',
        'title': "Ping IP Address",
        'target': fields.IPAddressField(
            required=True,
            widget=forms.TextInput(
                {'class': 'form-control'},
            ),
            label_suffix='',
            label='Target Address'
        ),
        'cmd': lambda target: "ping %s source Loopback0" % (str(target))
    },
    'trace_route': {
        'index': 3,
        'name': 'trace_route',
        'title': 'Traceroute to IP Address',
        'target': fields.IPAddressField(
            required=True,
            widget=forms.TextInput(
                {'class': 'form-control'},
            ),
            label_suffix='',
            label='Target Address'
        ),
        'cmd': lambda target: "traceroute %s" % (str(target))
    }
}

# Default salt value for authorisation key generation
SALT = '_signing_salt_'

# Link to Acceptable Use Policy
AUP_LINK = None

# Google reCapture settings
RECAPTCHA_ON = False
RECAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'

#################################################################
# Don't edit below this line!

try:
    from djangolg.local_settings import *
except Exception:
    pass
