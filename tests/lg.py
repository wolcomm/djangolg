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
"""Dummy Looking Glass command execution module for testing."""

from __future__ import print_function
from __future__ import unicode_literals

from djangolg import dialects, lg, models


class DummyDriver(object):
    """Dummy napalm-like driver for testing."""

    def __init__(self, hostname=None, username=None, password=None):
        """Initialise instance."""
        self.hostname = hostname
        self.username = username
        self.password = password

    def open(self):
        """Set up."""
        return True

    def __exit__(self, *args):
        """Tear down."""
        pass

    def cli(self, commands=None):
        """Execute fake cli method."""
        output = {}
        for command in commands:
            output[command] = "{0}: {1}".format(self.hostname, command)
        return output


class DummyLookingGlass(lg.LookingGlass):
    """Dummy Looking Glass execution class."""

    def __init__(self, router=None):
        """Initialise new LookingGlass instance."""
        if not isinstance(router, models.Router):
            raise ValueError
        self.dialect = dialects.get_dialect(router.dialect)
        self.device = DummyDriver(
            hostname=router.hostname,
            username=router.credentials.username,
            password=router.credentials.password)
