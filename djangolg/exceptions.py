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


class LookingGlassError(Exception):
    """Exception raised during looking glass query execution."""


class TypeCheckError(TypeError):
    """Exception raised by check_type helper."""


def check_type(instance=None, classinfo=None):
    """Raise an exception if object is not an instance of classinfo."""
    if not isinstance(instance, classinfo):
        raise TypeCheckError(
            "expected an instance of {0}, got {1}".format(classinfo, instance)
        )
