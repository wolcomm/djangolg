from __future__ import print_function
from __future__ import unicode_literals


class BaseMethod(object):
    name = None
    title = None
    new = False
    description = None
    target_field = None
    options = None

    def __init__(self, dialect=None):
        from djangolg.dialects.base import BaseDialect
        if dialect and not isinstance(dialect, BaseDialect):
            raise ValueError
        self._dialect = dialect

    @property
    def dialect(self):
        return self._dialect

    @dialect.setter
    def dialect(self, dialect=None):
        from djangolg.dialects.base import BaseDialect
        if not isinstance(dialect, BaseDialect):
            raise ValueError
        self._dialect = dialect

    @property
    def doc_description(self):
        return self.__doc__

    def option_choices(self):
        return ((self.options.index(option), option)
                for option in self.options)

    def select_option(self, index):
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
