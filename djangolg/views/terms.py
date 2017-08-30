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
"""Terms and Conditions view module for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.http import JsonResponse
from django.views.generic import View

from djangolg import forms, keys, models, settings
from djangolg.views.helpers import get_src


class AcceptTermsView(View):
    """Terms and Conditions view class."""

    def get(self, request):
        """Handle GET request."""
        response = {'status': 'error'}
        query = request.GET
        src_host = get_src(self.request)
        if query:
            if settings.RECAPTCHA_ON:
                recaptcha = {
                    'recaptcha_resp': query['g-recaptcha-response'],
                    'secret_key': settings.RECAPTCHA_SECRET_KEY,
                    'src_address': src_host
                }
                form = forms.RecaptchaTermsForm(recaptcha)
            else:
                form = forms.AcceptTermsForm(query)
            if form.is_valid():
                key = keys.AuthKey(get_src(self.request))
                models.Log(event=models.Log.EVENT_START, src_host=src_host,
                           key=key).save()
                response = {
                    'status': 'ok',
                    'key': key.signed
                }
            else:
                return JsonResponse({}, status=400)
        else:
            return JsonResponse({}, status=400)
        return JsonResponse(response)
