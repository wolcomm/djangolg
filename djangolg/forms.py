from django import forms
from djangolg import models, fields


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
    ipv4_src_address = fields.IPPrefixField(
        required=False,
        widget=forms.HiddenInput,
    )
    ipv6_src_address = fields.IPPrefixField(
        required=False,
        widget=forms.HiddenInput
    )


def form_factory(method=None, key=None, data=None):
    if method:
        class FormClass(LookingGlassBaseForm):
            method_name = forms.CharField(
                required=True,
                widget=forms.HiddenInput,
                initial=method.name
            )
            auth_key = forms.CharField(
                required=True,
                widget=forms.HiddenInput,
                initial=key
            )
            target = method.target
            if method.options:
                options = forms.ChoiceField(
                    required=True,
                    choices=method.option_choices,
                    widget=forms.RadioSelect(
                    ),
                    label_suffix='',
                    label='Options'
                )
        form = FormClass(data)
    else:
        form = LookingGlassBaseForm(data)
    return form
