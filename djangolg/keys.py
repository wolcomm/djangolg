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

from django.core.signing import SignatureExpired, TimestampSigner

from djangolg import events, exceptions, settings


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

    def validate(self, key, life=None):
        """Validate key value."""
        if not life and settings.LIFETIME:
            life = settings.LIFETIME
        try:
            clear = self.signer.unsign(key, max_age=life)
        except SignatureExpired as e:
            raise KeyValidityExpired("{}".format(e))
        if self.clear == clear:
            return True
        else:
            raise KeyValueMismatchError(keyval=clear, refval=self.clear)

    def __str__(self):
        """Return string representation."""
        return self.signed

    def __unicode__(self):
        """Return string representation."""
        return self.__str__()


class KeyValidationError(exceptions.LookingGlassError):
    """Generic exception raised if key validation fails."""

    http_status = 401
    http_reason = "An error occured during authorisation key validation. \
                   Please try again or contact support."
    log_event = events.EVENT_QUERY_REJECT


class KeyValueMismatchError(KeyValidationError):
    """Exception raised when key validation fails due to value mis-match."""

    http_reason = "Source address does not match authorisation key. \
                   Please try refreshing the page or contact support."

    def __init__(self, keyval=None, refval=None, *args, **kwargs):
        """Initialise new KeyValueMismatchError instance."""
        self.message = "decyrpted key value ({0}) does not match \
                        reference value ({1}).".format(keyval, refval)
        super(self.__class__, self).__init__(self.message, *args, **kwargs)


class KeyValidityExpired(KeyValidationError, SignatureExpired):
    """Exception raised when key signature has expired."""

    http_reason = "The authorisation key provided has expired. \
                   Please try refreshing the page or contact support"
