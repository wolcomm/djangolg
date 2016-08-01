from djangolg.local_settings import *
from django import forms
from djangolg import fields

# Lifetime of session authorisation key
LIFETIME = 300

# TODO: Implement database logging and max-requests checking
# Maximum number of requests with the same key
MAX_REQUESTS = 30

# TODO: Provide method "options"
# TODO: Provide dialect-specific cmd syntax
# Query methods, and their implementation variables
METHODS = {
    'bgp_prefix': {
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
        'options': {},
        'cmd': lambda target: "show bgp ipv%s unicast %s" % (target.version, str(target))
    },
    'bgp_as_path': {
        'name': 'bgp_as_path',
        'title': "BGP AS_PATH Query",
        'target': forms.CharField(
            required=True,
            widget=forms.TextInput(
                {'class': 'form-control'}
            ),
            label_suffix='',
            label='AS Path Regex'
        ),
        'options': {},
        'cmd': lambda target: "show bgp %s unicast regex %s" % ('ipv4', str(target))
    },
}
