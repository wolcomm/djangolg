from django import forms as _forms
from djangolg import forms, fields

# TODO: Move _methods into settings
_methods = {
    'bgp_prefix': {
        'name': 'bgp_prefix',
        'form': forms.BGPPrefixForm,
        'title': "BGP Prefix Query",
        'target': fields.IPPrefixField(
            required=True,
            widget=_forms.TextInput(
                {'class': 'form-control'}
            ),
            label_suffix='',
            label='Prefix'
        ),
        'options': {},
        'cmd': "show bgp %s unicast %s"
    },
    'bgp_as_path': {
        'name': 'bgp_as_path',
        'form': forms.BGPAsPathForm,
        'title': "BGP AS_PATH Query",
        'target': _forms.CharField(
            required=True,
            widget=_forms.TextInput(
                {'class': 'form-control'}
            ),
            label_suffix='',
            label='AS Path Regex'
        ),
        'options': {},
        'cmd': "show bgp %s unicast regex %s"
    },
}


def methods():
    return _methods.keys()


class Method(object):
    def __init__(self, method):
        if method in _methods:
            self.method = _methods[method]

    @property
    def name(self):
        return self.method['name']

    @property
    def form(self):
        return self.method['form']

    @property
    def title(self):
        return self.method['title']

    @property
    def target(self):
        return self.method['target']

    @property
    def options(self):
        return self.method['options']

    @property
    def cmd(self):
        return self.method['cmd']
