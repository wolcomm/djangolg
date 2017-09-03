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

# from djangolg import views
from djangolg.views import helpers


class ViewHelpersCase(TestCase):
    """Test djangolg view helper functions."""

    def test_get_src_helper(self):
        """Test get_src helper."""
        try:
            helpers.get_src()
        except Exception as e:
            assert isinstance(e, TypeError)
