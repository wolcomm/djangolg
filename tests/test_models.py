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
"""Model test classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.test import TestCase

from djangolg import events, models


class ModelTestCase(TestCase):
    """Test djangolg models."""

    def setUp(self):
        """Create the necessary objects."""
        credentials = models.Credential.objects.create(
            name="test-credentials", type=models.Credential.CRED_TYPE_PASSWD,
            username="test", password="test"
        )
        location = models.Location.objects.create(
            name="test-location", sitecode="test01"
        )
        router = models.Router.objects.create(
            hostname="test-router", dialect="ios",
            location=location, credentials=credentials
        )
        models.Log.objects.create(
            event=events.EVENT_START,
            src_host="::1", router=router,
            error="test-log-error"
        )

    def test_credentials(self):
        """Test getting credentials by name and returning properties."""
        credentials = models.Credential.objects.get(name="test-credentials")
        assert "{}".format(credentials) == "test-credentials"

    def test_location(self):
        """Test getting location by name and returning properties."""
        location = models.Location.objects.get(name="test-location")
        assert "{}".format(location) == "test01"

    def test_router(self):
        """Test getting router by name and returning properties."""
        router = models.Router.objects.get(hostname="test-router")
        assert "{}".format(router) == "test-router"
        assert router.label == "test-location"

    def test_log(self):
        """Test getting log entry by (event, error) pair."""
        log = models.Log.objects.get(event=events.EVENT_START,
                                     error="test-log-error")
        timestamp = "{}".format(log.timestamp)
        assert timestamp in "{}".format(log)
        assert "test-log-error" in "{}".format(log)
