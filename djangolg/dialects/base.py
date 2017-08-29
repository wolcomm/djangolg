import napalm
import inspect
from napalm_base import NetworkDriver


class BaseDialect(object):
    """Device dialect class"""
    driver_class = None
    name = None
    description = None
    commands = {}

    def __init__(self):
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
