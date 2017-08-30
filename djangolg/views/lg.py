from __future__ import print_function
from __future__ import unicode_literals

from django.views.generic import View
from django.http import JsonResponse
from djangolg import forms, methods, keys, models, settings
from djangolg.lg import LookingGlass
from djangolg.views.helpers import get_src


class LookingGlassJsonView(View):
    def get(self, request):
        query = request.GET
        if not query:
            return JsonResponse({}, status=400)
        self.src_host = get_src(self.request)
        self.key = query['auth_key']
        log = models.Log(src_host=self.src_host)
        log.key = self.key
        if self.authorise():
            log.event = models.Log.EVENT_QUERY_ACCEPT
            self.method = methods.get_method(query['method_name'])
            if self.method:
                log.method_name = self.method.name
                self.form = forms.form_factory(method=self.method, data=query)
                if self.form.is_valid():
                    log.router = self.form.cleaned_data['router']
                    log.target = self.form.cleaned_data['target']
                    data = self.execute()
                    resp = JsonResponse(data)
                else:
                    log.event = models.Log.EVENT_QUERY_INVALID
                    log.error = 'form validation failure'
            else:
                log.event = models.Log.EVENT_QUERY_INVALID
                log.error = "invalid method name"
        else:
            log.event = models.Log.EVENT_QUERY_REJECT
            log.error = "invalid or expired authorisation key - \
                         refresh the page to retry"
        if log.event != models.Log.EVENT_QUERY_ACCEPT:
            resp = JsonResponse({}, status=400, reason=log.error)
        log.save()
        return resp

    def authorise(self):
        if not self.src_host:
            raise RuntimeError("src_host not set")
        if not self.key:
            raise RuntimeError("auth_key not set")
        if keys.AuthKey(self.src_host).validate(self.key):
            count = models.Log.objects.filter(key=self.key).count()
            if not settings.MAX_REQUESTS or count < settings.MAX_REQUESTS:
                return True
        return False

    def execute(self):
        if not self.form:
            raise RuntimeError("form not set")
        if not self.method:
            raise RuntimeError("method not set")
        data = self.form.cleaned_data
        router = data['router']
        target = data['target']
        if 'options' in data:
            option_index = int(data['options'])
        else:
            option_index = None
        with LookingGlass(router=router) as lg:
            output = lg.execute(
                method=self.method,
                target=target,
                option_index=option_index
            )
        return output
