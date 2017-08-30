from __future__ import print_function
from __future__ import unicode_literals

from django.views.generic import View
from django.http import JsonResponse
from djangolg import forms, keys, models, settings
from djangolg.views.helpers import get_src


class AcceptTermsView(View):
    def get(self, request):
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
