from __future__ import print_function
from __future__ import unicode_literals

from djangolg import dialects, models


class LookingGlass(object):
    def __init__(self, router=None):
        if not isinstance(router, models.Router):
            raise ValueError
        self.dialect = dialects.get_dialect(router.dialect)
        self.device = self.dialect.driver_class(
            hostname=router.hostname,
            username=router.credentials.username,
            password=router.credentials.password)

    def __enter__(self):
        self.device.open()
        return self

    def __exit__(self, *args):
        self.device.__exit__(*args)

    def execute(self, method=None, target=None, option_index=None):
        output = {}
        method.dialect = self.dialect
        command = method.get_command(target=target, option_index=option_index)
        tmp = self.device.cli([command])
        raw = tmp[command]
        output['raw'] = raw
        return output
