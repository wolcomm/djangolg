# Copyright 2017 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
from __future__ import print_function
from __future__ import unicode_literals

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
        if not response['success']:
            raise forms.ValidationError
        else:
            return


class RouterSelectForm(forms.Form):
    router = fields.RouterChoiceField(
        required=True,
        queryset=models.Router.objects.all(),
        widget=forms.Select(
            attrs={
                'id': "router-select",
                'class': 'form-control',
                'data-toggle': 'tooltip',
                'title': "Select a router to query"
            }
        ),
        empty_label="Select Router"
    )


class LookingGlassBaseForm(forms.Form):
    router = forms.ModelChoiceField(
        required=True,
        queryset=models.Router.objects.all(),
        widget=forms.HiddenInput,
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
            target = method.target_field
            if method.options:
                options = forms.ChoiceField(
                    required=True,
                    choices=method.option_choices,
                    widget=forms.RadioSelect(),
                    initial=0,
                )
        form = FormClass(data, prefix=prefix)
    else:
        form = LookingGlassBaseForm(data, prefix=prefix)
    return form
