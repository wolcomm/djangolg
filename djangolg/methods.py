from djangolg import settings


def methods():
    M = sorted(settings.METHODS.items(), key=lambda m: m[1]['index'])
    return [m[0] for m in M]


def dialects():
    D = sorted(settings.DIALECTS.items(), key=lambda d: d[1]['index'])
    return [d[0] for d in D]


def dialect_choices():
    return [(d, Dialect(d).name) for d in dialects()]


class Method(object):
    def __init__(self, method):
        if method in methods():
            self.method = settings.METHODS[method]
        else:
            raise KeyError
        self._dialect = None

    @property
    def dialect(self):
        return self._dialect

    @dialect.setter
    def dialect(self, dialect=None):
        if self.name in dialect.cmds:
            self._dialect = dialect
        else:
            raise NotImplementedError
        return self

    @property
    def name(self):
        return self.method['name']

    @property
    def title(self):
        return self.method['title']

    @property
    def description(self):
        return self.method['description']

    @property
    def target(self):
        return self.method['target']

    @property
    def options(self):
        if self.dialect:
            if 'options' in self.dialect.cmds[self.name]:
                return self.dialect.cmds[self.name]['options']
        else:
            if 'options' in self.method:
                return self.method['options']
        return []

    @property
    def option_choices(self):
        return ( (self.options.index(option), option['label']) for option in self.options )

    @property
    def cmd(self):
        if self.dialect:
            return self.dialect.cmds[self.name]['cmd']
        else:
            return self.method['cmd']

    @property
    def template(self):
        if self.dialect:
            return self.dialect.cmds[self.name]['template']
        else:
            return self.method['template']


class Dialect(object):
    def __init__(self, dialect):
        if dialect in dialects():
            self._dialect = settings.DIALECTS[dialect]
        else:
            raise KeyError
        self._str = dialect

    @property
    def index(self):
        return self._dialect['index']

    @property
    def name(self):
        return self._dialect['name']

    @property
    def cmds(self):
        return self._dialect['cmds']

    def __str__(self):
        return self._str
