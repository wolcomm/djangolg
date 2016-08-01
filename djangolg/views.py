from django.views.generic import View, TemplateView
from django.http import JsonResponse
from djangolg import forms, methods, keys, models, settings
from djangolg.lg import LookingGlass


class IndexView(TemplateView):
    template_name = 'djangolg/lg.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        key = keys.AuthKey(self.request.get_host())
        context['methods'] = []
        for m in methods.methods():
            method = methods.Method(m)
            form = forms.form_factory(method=method, key=key)
            context['methods'].append({'method': method, 'form': form})
        return context


class LookingGlassHTMLView(TemplateView):
    template_name = "djangolg/output.html"

    def get_context_data(self, **kwargs):
        context = super(LookingGlassHTMLView, self).get_context_data(**kwargs)
        query = self.request.GET
        src_host = self.request.get_host()
        log = models.Log(src_host=src_host)
        if query:
            key = query['auth_key']
            log.key = key
            if self.authorise(key=key, src_host=src_host):
                log.event = models.Log.EVENT_QUERY_ACCEPT
                method = methods.Method(query['method_name'])
                if method:
                    log.method_name = method.name
                    form = forms.form_factory(method=method, data=query)
                    if form.is_valid():
                        log.router = form.cleaned_data['router']
                        log.target = form.cleaned_data['target']
                        context['output'] = self.execute(form=form, method=method)
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

    def authorise(self, key=None, src_host=None):
        if keys.AuthKey(src_host).validate(key):
            count = models.Log.objects.filter(key=key).count()
            if not settings.MAX_REQUESTS or count < settings.MAX_REQUESTS:
                return True
        return False

    def execute(self, form, method):
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
        )
        return output


class LookingGlassJsonView(View):
    def get(self, request):
        query = request.GET
        if not query:
            return JsonResponse({}, status=400)
        method = methods.Method(query['method_name'])
        if method:
            form = method.form(query)
            if form.is_valid():
                response = { 'output': form.execute() }
            else:
                response = { 'output': 'Error' }
        else:
            response = { 'output': 'Bad Command' }
        return JsonResponse(response)
