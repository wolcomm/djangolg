from django import forms
from djangolg import models, fields
from djangolg.lg import LookingGlass


class LookingGlassBaseForm(forms.Form):
    label_suffix = ''
    router = forms.ModelChoiceField(
        required=True,
        queryset=models.Router.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        label_suffix=label_suffix,
    )
    prefix = fields.IPPrefixField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        label_suffix=label_suffix
    )
    longer_prefixes = forms.BooleanField(
        required=False,
        label_suffix=label_suffix
    )
    bestpath_only = forms.BooleanField(
        required=False,
        label_suffix=label_suffix
    )
    ipv4_src_address = fields.IPPrefixField(
        required=False,
        widget=forms.HiddenInput,
    )
    ipv6_src_address = fields.IPPrefixField(
        required=False,
        widget=forms.HiddenInput
    )


class BGPPrefixForm(LookingGlassBaseForm):
    def execute(self):
        data = self.cleaned_data
        lg = LookingGlass(data['router'])
        prefix = data['prefix']
        longer_prefixes = data['longer_prefixes']
        bestpath_only = data['bestpath_only']
        output = lg.bgp_prefix(prefix, longer_prefixes, bestpath_only)
        return output


class BGPAsPathForm(LookingGlassBaseForm):
    def execute(self):
        data = self.cleaned_data
        lg = LookingGlass(data['router'])
        prefix = data['prefix']
        longer_prefixes = data['longer_prefixes']
        bestpath_only = data['bestpath_only']
        output = lg.bgp_prefix(prefix, longer_prefixes, bestpath_only)
        return output


class NewLookingGlassBaseForm(forms.Form):
    label_suffix = ''
    method = None
    router = forms.ModelChoiceField(
        required=True,
        queryset=models.Router.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        label_suffix=label_suffix,
    )
    ipv4_src_address = fields.IPPrefixField(
        required=False,
        widget=forms.HiddenInput,
    )
    ipv6_src_address = fields.IPPrefixField(
        required=False,
        widget=forms.HiddenInput
    )


def form_factory(method=None, data={}):
    class FormClass(NewLookingGlassBaseForm):
        if method:
            target = method.target
    form = FormClass(data)
    return form
