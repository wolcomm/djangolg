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
"""Cryptographic key classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.core.signing import TimestampSigner

from djangolg import settings


class AuthKey(object):
    """Command authorisation key class."""

    def __init__(self, value=None):
        """Initialise new AuthKey instance."""
        self.signer = TimestampSigner(salt="auth")
        self._data = {
            'clear': value,
            'signed': self.signer.sign(value)
        }

    @property
    def clear(self):
        """Get cleartext key value."""
        return self._data['clear']

    @property
    def signed(self):
        """Get cyphertext key value."""
        return self._data['signed']

    def validate(self, key):
        """Validate key value."""
        life = None
        if settings.LIFETIME:
            life = settings.LIFETIME
        try:
            clear = self.signer.unsign(key, max_age=life)
            if self.clear == clear:
                return True
            else:
                return False
        except Exception:
            return False
        return False

    def __str__(self):
        """Return string representation."""
        return self.signed

    def __unicode__(self):
        """Return string representation."""
        return self.__str__()
