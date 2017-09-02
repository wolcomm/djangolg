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
"""Base exception classes and helpers for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from djangolg import events


DEFAULT_EVENT = events.EVENT_QUERY_ERROR
DEFAULT_STATUS = 500
DEFAULT_REASON = "An unhandled error occured. \
                  Please try again or contact support."


class LookingGlassError(Exception):
    """Exception raised during looking glass query execution."""

    log_event = DEFAULT_EVENT
    http_status = DEFAULT_STATUS
    http_reason = DEFAULT_REASON
    response_data = {}

    @property
    def log_error(self):
        """Render the log message for this exception."""
        return default_error_message(self)


class TypeCheckError(TypeError):
    """Exception raised by check_type helper."""


def check_type(instance=None, classinfo=None):
    """Raise an exception if object is not an instance of classinfo."""
    if not isinstance(instance, classinfo):
        raise TypeCheckError(
            "expected an instance of {0}, got {1}".format(classinfo, instance)
        )


def default_error_message(e=None):
    """Generate a default log message from an exception."""
    check_type(instance=e, classinfo=Exception)
    return "{0}: {1}".format(e.__class__.__name__, e)
