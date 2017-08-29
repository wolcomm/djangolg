import os
import napalm
import textfsm
from djangolg import methods, dialects, settings, models


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

    def _build_cmd(self, method, target=None, option=None):
        if self.dialect:
            try:
                method.dialect = self.dialect
            except NotImplementedError:
                pass
        if method.options and isinstance(option, int):
            cmd = method.options[option]['cmd'](target)
        else:
            cmd = method.cmd(target)
        return cmd

    def _parse(self, raw, method, option=None):
        templates_dir = settings.TEXTFSM_TEMPLATES_DIR
        if self.dialect:
            templates_dir = os.path.join(templates_dir, str(self.dialect))
            try:
                method.dialect = self.dialect
            except NotImplementedError:
                pass
        try:
            if method.options and isinstance(option, int):
                template = method.options[option]['template']
            else:
                template = method.template
        except KeyError:
            return None
        try:
            f = os.path.join(templates_dir, template)
            t = open(f)
        except:
            raise
        parser = textfsm.TextFSM(t)
        parsed = {
            'header': parser.header,
            'data': parser.ParseText(raw)
        }
        return parsed

    def execute(self, method=None, target=None, option_index=None, parse=False):
        # cmd = self._build_cmd(method, target=target, option=option)
        output = {}
        method.dialect = self.dialect
        command = method.get_command(target=target, option_index=option_index)
        tmp = self.device.cli([command])
        raw = tmp[command]
        output['raw'] = raw
        # if parse:
        #     parsed = self._parse(raw=raw, method=method, option=option)
        #     output['parsed'] = parsed
        return output
