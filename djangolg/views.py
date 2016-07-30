from django.views.generic import View, TemplateView
from django.http import JsonResponse
from djangolg import forms, methods


class IndexView(TemplateView):
    template_name = 'djangolg/lg.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['methods'] = []
        for m in methods.methods():
            method = methods.Method(m)
            form = method.form()
            context['methods'].append({ 'method': method, 'form': form })
        return context


class LookingGlassJsonView(View):
    def get(self, request, method=None):
        query = request.GET
        if not query:
            return JsonResponse({}, status=400)
        method = methods.Method(method)
        if method:
            form = method.form(query)
            if form.is_valid():
                response = { 'output': form.execute() }
            else:
                response = { 'output': 'Error' }
        else:
            response = { 'output': 'Bad Command' }
        return JsonResponse(response)


class LookingGlassHTMLView(TemplateView):
    template_name = "djangolg/output.html"
    def get_context_data(self, **kwargs):
        context = super(LookingGlassHTMLView, self).get_context_data(**kwargs)
        query = self.request.GET
        if query:
            method = methods.Method(kwargs["method"])
            if method:
                form = method.form(query)
                if form.is_valid():
                    context['output'] = form.execute()
                else:
                    context['output'] = 'Error'
            else:
                context['output'] = 'Bad Command'
        return context
