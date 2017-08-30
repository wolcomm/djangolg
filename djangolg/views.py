from __future__ import print_function
from __future__ import unicode_literals

from django.views.generic import View, TemplateView
from django.http import JsonResponse
from djangolg import forms, methods, keys, models, settings
from djangolg.lg import LookingGlass


class IndexView(TemplateView):
    template_name = 'djangolg/lg.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['base_template'] = settings.BASE_TEMPLATE
        context['info'] = self.general_info()
        context['recaptcha'] = self.recaptcha()
        context['methods'] = []
        for method_name in methods.available_methods(output="list"):
            method = methods.get_method(name=method_name)
            form = forms.form_factory(method=method)
            context['methods'].append({'method': method, 'form': form})
        context['modal'] = forms.AcceptTermsForm()
        context['router_select'] = forms.RouterSelectForm()
        return context

    def general_info(self):
        info = {
            'name': settings.NETNAME,
            'title': "%s Looking Glass" % settings.NETNAME,
            'general_email': settings.GENERAL_EMAIL,
            'support_email': settings.SUPPORT_EMAIL,
            'noc_email': settings.NOC_EMAIL,
            'peering_email': settings.PEERING_EMAIL,
            'aup_link': settings.AUP_LINK,
            'src_address': get_src(self.request),
            'logo': settings.LOGO,
            'small_logo': settings.SMALL_LOGO,
            'favicon': settings.FAVICON,
            'nav_img': settings.NAV_IMG,
            'formatted': settings.FORMATTED_OUTPUT
        }
        return info

    def recaptcha(self):
        if settings.RECAPTCHA_ON:
            return {'site_key': settings.RECAPTCHA_SITE_KEY}
        else:
            return None


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
            method = methods.get_method(query['method_name'])
            if method:
                log.method_name = method.name
                form = forms.form_factory(method=method, data=query)
                if form.is_valid():
                    log.router = form.cleaned_data['router']
                    log.target = form.cleaned_data['target']
                    data = execute(form=form, method=method)
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


def get_src(request=None):
    address = None
    if request.META:
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            address = "{0}"\
                .format(request.META['HTTP_X_FORWARDED_FOR'].split(',')[0])
        else:
            address = "{0}".format(request.META['REMOTE_ADDR'])
    return address


def execute(form, method):
    data = form.cleaned_data
    router = data['router']
    target = data['target']
    if 'options' in data:
        option_index = int(data['options'])
    else:
        option_index = None
    with LookingGlass(router=router) as lg:
        output = lg.execute(
            method=method,
            target=target,
            option_index=option_index
        )
    return output
