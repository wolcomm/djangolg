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

from django.test import Client, TestCase
from django.urls import reverse

from djangolg import settings
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
        client = Client()
        url = reverse('djangolg-index')
        settings.RECAPTCHA_ON = False
        response = client.get(url)
        assert response.status_code == 200
        settings.RECAPTCHA_ON = True
        response = client.get(url)
        assert response.status_code == 200

    def test_index_view_with_proxy(self):
        """Test index view with the HTTP_X_FORWARDED_FOR header set."""
        client = Client()
        url = reverse('djangolg-index')
        extra = {'HTTP_X_FORWARDED_FOR': '192.0.2.1'}
        settings.RECAPTCHA_ON = False
        response = client.get(url, **extra)
        assert response.status_code == 200
        settings.RECAPTCHA_ON = True
        response = client.get(url, **extra)
        assert response.status_code == 200

    def test_std_terms_view(self):
        """Test terms view."""
        client = Client()
        url = reverse('djangolg-enter')
        settings.RECAPTCHA_ON = False
        response = client.get(url)
        assert response.status_code == 400
        response = client.get(url, {'accept': 'on'})
        assert response.status_code == 200

    def test_recapture_terms_view(self):
        """Test terms view."""
        client = Client()
        url = reverse('djangolg-enter')
        query = {'g-recaptcha-response': 'dummy_response'}
        settings.RECAPTCHA_ON = True
        response = client.get(url)
        assert response.status_code == 400
        response = client.get(url, query)
        assert response.status_code == 400
        settings.RECAPTCHA_SECRET_KEY = 'dummy_key'
        response = client.get(url, query)
        assert response.status_code == 200
