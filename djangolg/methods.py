from djangolg import forms

_methods = {
    'bgp_prefix': {
        'name': 'bgp_prefix',
        'form': forms.BGPPrefixForm,
        'title': "BGP Prefix Query",
    }
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
