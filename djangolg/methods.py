from django import forms
from djangolg import fields

# TODO: Move _methods into settings
# TODO: Provide method "options"
# TODO: Provide dialect-specific cmd syntax
_methods = {
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
