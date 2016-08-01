from djangolg.local_settings import *
from django import forms
from djangolg import fields

# TODO: Provide method "options"
# TODO: Provide dialect-specific cmd syntax
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
