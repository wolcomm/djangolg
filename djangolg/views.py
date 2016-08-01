from django.views.generic import View, TemplateView
from django.http import JsonResponse
from djangolg import forms, methods, keys
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
        if query:
            key = query['auth_key']
            if keys.AuthKey(self.request.get_host()).validate(key):
                method = methods.Method(query['method_name'])
                if method:
                    form = forms.form_factory(method=method, data=query)
                    if form.is_valid():
                        context['output'] = self.execute(form=form, method=method)
                    else:
                        context['output'] = 'Error'
                else:
                    context['output'] = 'Bad Command'
            else:
                context['output'] = 'Invalid Auth Key'
        return context

    def execute(self, form, method):
        data = form.cleaned_data
        lg = LookingGlass(data['router'])
        output = lg.execute(
            method=method,
            target=data['target'],
            # options=data['options']
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
