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
"""Base dialect class for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

import inspect

import napalm

from napalm_base import NetworkDriver


class BaseDialect(object):
    """Device base dialect class."""

    driver_class = None
    name = None
    description = None
    commands = {}

    def __init__(self):
        """Initialise new instance."""
        if not isinstance(self.driver_class, NetworkDriver):
            if type(self).name:
                self.driver_class = napalm.get_network_driver(type(self).name)
            else:
                raise ValueError

    def get_command_syntax(self, method=None, option=None):
        """Get the dialect specific syntax for a given method as a lambda."""
        from djangolg.methods.base import BaseMethod
        if not isinstance(method, BaseMethod):
            return ValueError
        syntax = None
        if method.name in self.commands:
            if option is not None:
                if option in self.commands[method.name]:
                    syntax = self.commands[method.name][option]
            else:
                syntax = self.commands[method.name]
        if syntax:
            if inspect.isfunction(syntax):
                return syntax
            else:
                raise TypeError
        raise NotImplementedError
