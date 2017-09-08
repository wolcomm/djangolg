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
"""View test classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from djangolg import keys, methods, models, settings
from djangolg.views import helpers


class ViewHelpersCase(TestCase):
    """Test djangolg view helper functions."""

    def test_get_src_helper(self):
        """Test get_src helper."""
        try:
            helpers.get_src()
        except Exception as e:
            assert isinstance(e, TypeError)


class ViewsTestCase(TestCase):
    """Test djangolg index view."""

    def test_index_view(self):
        """Test index view."""
        url = reverse('djangolg-index')
        settings.RECAPTCHA_ON = False
        response = self.client.get(url)
        assert response.status_code == 200
        settings.RECAPTCHA_ON = True
        response = self.client.get(url)
        assert response.status_code == 200

    def test_index_view_with_proxy(self):
        """Test index view with the HTTP_X_FORWARDED_FOR header set."""
        url = reverse('djangolg-index')
        extra = {'HTTP_X_FORWARDED_FOR': '192.0.2.1'}
        settings.RECAPTCHA_ON = False
        response = self.client.get(url, **extra)
        assert response.status_code == 200
        settings.RECAPTCHA_ON = True
        response = self.client.get(url, **extra)
        assert response.status_code == 200

    def test_std_terms_view(self):
        """Test terms view."""
        url = reverse('djangolg-enter')
        settings.RECAPTCHA_ON = False
        response = self.client.get(url)
        assert response.status_code == 400
        response = self.client.get(url, {'accept': 'on'})
        assert response.status_code == 200

    def test_recapture_terms_view(self):
        """Test terms view."""
        url = reverse('djangolg-enter')
        query = {'g-recaptcha-response': 'dummy_response'}
        settings.RECAPTCHA_ON = True
        response = self.client.get(url)
        assert response.status_code == 400
        response = self.client.get(url, query)
        assert response.status_code == 400
        settings.RECAPTCHA_SECRET_KEY = 'dummy_key'
        response = self.client.get(url, query)
        assert response.status_code == 200

    def test_lg_view(self):
        """Test lg view."""
        router = models.Router.objects.create(hostname="test-router")
        src_addr = '192.0.2.1'
        auth_key = keys.AuthKey(value=src_addr).signed
        url = reverse('djangolg-lg')
        extra = {'HTTP_X_FORWARDED_FOR': src_addr}
        for method_name in methods.available_methods(output="list"):
            method = methods.get_method(name=method_name)
            query = {'method_name': method_name}
            response = self.client.get(url, query, **extra)
            assert response.status_code == 400  # QueryParsingError
            assert "Bad Request" in response.reason_phrase
            query['auth_key'] = keys.AuthKey(value='192.0.2.255').signed
            response = self.client.get(url, query, **extra)
            assert response.status_code == 401  # KeyValidationError
            assert "does not match authorisation key" in response.reason_phrase
            query['auth_key'] = 'bad_key'
            response = self.client.get(url, query, **extra)
            assert response.status_code == 401  # AuthorisationError
            assert "command authorisation" in response.reason_phrase
            query['auth_key'] = auth_key
            response = self.client.get(url, query, **extra)
            assert response.status_code == 400  # FormValidationError
            assert "parameters failed to validate" in response.reason_phrase
            query['router'] = router.id
            query['target'] = "{}".format(method.test_target)
            if method.options:
                query['options'] = 0
            response = self.client.get(url, query, **extra)
            assert response.status_code == 503  # ExecutionError
            assert "during query execution" in response.reason_phrase
