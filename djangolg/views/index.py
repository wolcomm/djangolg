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

from django.views.generic import TemplateView
from djangolg import forms, methods, settings
from djangolg.views.helpers import get_src


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
