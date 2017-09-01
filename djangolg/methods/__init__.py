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
"""Method definitions and exceptions for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from djangolg import events, exceptions
from djangolg.methods.builtin import ( #noqa
    BGPPrefixMethod,
    BGPASPathMethod,
    BGPCommunityMethod,
    PingMethod,
    TracerouteMethod
)


def available_methods(output="map"):
    """Get available method classes."""
    from djangolg.methods.base import BaseMethod
    classes = BaseMethod.__subclasses__()
    if output == "map":
        return {m.name: m for m in classes}
    if output == "list":
        return [m.name for m in classes]
    else:
        raise ValueError("invalid output type: {0}".format(output))


def get_method(name=None):
    """Instantiate a method class by name."""
    try:
        return available_methods(output="map")[name]()
    except KeyError:
        raise MethodNotFound(name=name)
    except Exception as e:
        raise LookingGlassMethodError(e.message)


class LookingGlassMethodError(exceptions.LookingGlassError):
    """Generic exception raised by method classes and helpers."""

    log_event = events.EVENT_QUERY_ERROR
    http_status = 500
    http_reason = None


class MethodNotFound(LookingGlassMethodError):
    """Exception raised when a method matching a given name cannot be found."""

    log_event = events.EVENT_QUERY_INVALID
    http_status = 400

    def __init__(self, name=None, *args, **kwargs):
        """Initialise new MethodNotFound instance."""
        self.message = "No method class found with name {0}".format(name)
        super(self.__class__).__init__(self.message, *args, **kwargs)
