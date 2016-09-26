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
        for m in methods.methods():
            method = methods.Method(m)
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
            'nav_img': settings.NAV_IMG,
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
                log = models.Log(
                    event=models.Log.EVENT_START,
                    src_host=src_host,
                    key=key
                ).save()
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
        src_host = get_src(self.request)
        log = models.Log(src_host=src_host)
        key = query['auth_key']
        log.key = key
        if authorise(key=key, src_host=src_host):
            log.event = models.Log.EVENT_QUERY_ACCEPT
            method = methods.Method(query['method_name'])
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
            log.error = 'invalid authorisation key'
        if log.event != models.Log.EVENT_QUERY_ACCEPT:
            resp = JsonResponse({}, status=400, reason=log.error)
        log.save()
        return resp


class LookingGlassHTMLView(TemplateView):
    template_name = "djangolg/output.html"

    def get_context_data(self, **kwargs):
        context = super(LookingGlassHTMLView, self).get_context_data(**kwargs)
        query = self.request.GET
        src_host = get_src(self.request)
        log = models.Log(src_host=src_host)
        if query:
            key = query['auth_key']
            log.key = key
            if authorise(key=key, src_host=src_host):
                log.event = models.Log.EVENT_QUERY_ACCEPT
                method = methods.Method(query['method_name'])
                if method:
                    log.method_name = method.name
                    form = forms.form_factory(method=method, data=query)
                    if form.is_valid():
                        log.router = form.cleaned_data['router']
                        log.target = form.cleaned_data['target']
                        context['output'] = execute(form=form, method=method)
                    else:
                        log.event = models.Log.EVENT_QUERY_INVALID
                        log.error = "Form validation failed"
                        context['output'] = 'Error'
                else:
                    log.event = models.Log.EVENT_QUERY_INVALID
                    log.error = "Invalid method name"
                    context['output'] = 'Bad Command'
            else:
                log.event = models.Log.EVENT_QUERY_REJECT
                context['output'] = 'Invalid Auth Key'
        log.save()
        return context


def get_src(request=None):
    address = None
    if request.META:
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            address = unicode(request.META['HTTP_X_FORWARDED_FOR'].split(',')[0])
        else:
            address = unicode(request.META['REMOTE_ADDR'])
    return address


def authorise(key=None, src_host=None):
    if keys.AuthKey(src_host).validate(key):
        count = models.Log.objects.filter(key=key).count()
        if not settings.MAX_REQUESTS or count < settings.MAX_REQUESTS:
            return True
    return False


def execute(form, method):
    data = form.cleaned_data
    router = data['router']
    target = data['target']
    if 'options' in data:
        option = int(data['options'])
    else:
        option = None
    lg = LookingGlass(router=router)
    output = lg.execute(
        method=method,
        target=target,
        option=option,
        parse=True
    )
    return output
