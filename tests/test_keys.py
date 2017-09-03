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
"""Key test classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

import time

from django.test import TestCase

from djangolg import keys


class KeyTestCase(TestCase):
    """Test djangolg keys."""

    def test_validate_auth_key(self):
        """Test AuthKey validation."""
        value = "good_value"
        other_value = "bad_value"
        key = keys.AuthKey(value=value)
        other_key = keys.AuthKey(value=other_value)
        assert key.validate(key="{}".format(key))
        time.sleep(1)
        try:
            key.validate(key="{}".format(key), life=1)
        except Exception as e:
            assert isinstance(e, keys.KeyValidityExpired)
        try:
            other_key.validate(key="{}".format(key))
        except Exception as e:
            assert isinstance(e, keys.KeyValueMismatchError)
