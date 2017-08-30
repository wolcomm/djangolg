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
"""Base method class for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals


class BaseMethod(object):
    """Base method class."""

    name = None
    title = None
    new = False
    description = None
    target_field = None
    options = None

    def __init__(self, dialect=None):
        """Initialise new instance."""
        from djangolg.dialects.base import BaseDialect
        if dialect and not isinstance(dialect, BaseDialect):
            raise ValueError
        self._dialect = dialect

    @property
    def dialect(self):
        """Get dialect."""
        return self._dialect

    @dialect.setter
    def dialect(self, dialect=None):
        """Set dialect."""
        from djangolg.dialects.base import BaseDialect
        if not isinstance(dialect, BaseDialect):
            raise ValueError
        self._dialect = dialect

    def option_choices(self):
        """Get available options."""
        return ((self.options.index(option), option)
                for option in self.options)

    def select_option(self, index):
        """Get option name by index."""
        if self.options:
            return self.options[index]
        else:
            return None

    def get_command(self, target=None, option_index=None):
        """Get the dialect specific command syntax and return command."""
        option = self.select_option(index=option_index)
        syntax_function = self.dialect.get_command_syntax(method=self,
                                                          option=option)
        command = syntax_function(target=target)
        return command
