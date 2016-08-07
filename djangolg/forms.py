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
    src_address = fields.IPAddressField()

    def clean(self):
        super(RecaptchaTermsForm, self).clean()
        url = settings.RECAPTCHA_URL
        params = {
            'secret': self.data['secret_key'],
            'response': self.data['recaptcha_resp'],
            'remoteip': self.data['src_address'],
        }
        response = requests.get(url, params=params, verify=True).json()
        if not response['success'] == True:
            raise forms.ValidationError
        else:
            return


class LookingGlassBaseForm(forms.Form):
    label_suffix = ''
    router = forms.ModelChoiceField(
        required=True,
        queryset=models.Router.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        label_suffix=label_suffix,
        empty_label="Select Router"
    )
    ipv4_src_address = fields.IPPrefixField(
        required=False,
        widget=forms.HiddenInput,
    )
    ipv6_src_address = fields.IPPrefixField(
        required=False,
        widget=forms.HiddenInput
    )


def form_factory(method=None, data=None, prefix=None):
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
        form = FormClass(data, prefix=prefix)
    else:
        form = LookingGlassBaseForm(data, prefix=prefix)
    return form
