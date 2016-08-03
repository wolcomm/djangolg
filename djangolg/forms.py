import requests
from django import forms
from djangolg import models, fields, settings


class AcceptTermsForm(forms.Form):
    label_suffix = ''
    accept = forms.BooleanField(
        required=True,
        label_suffix='',
        label="I have read and accept the terms of use"
    )


class RecaptchaTermsForm(forms.Form):
    recaptcha_resp = forms.CharField()
    secret_key = forms.CharField()
    def clean(self):
        super(RecaptchaTermsForm, self).clean()


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


def form_factory(method=None, data=None):
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
            )
            target = method.target
            if method.options:
                options = forms.ChoiceField(
                    required=True,
                    choices=method.option_choices,
                    widget=forms.RadioSelect(),
                    label_suffix='',
                    label='Options',
                    initial=0,
                )
        form = FormClass(data)
    else:
        form = LookingGlassBaseForm(data)
    return form
