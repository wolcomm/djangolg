from djangolg import settings


def methods():
    M = sorted(settings.METHODS.items(), key=lambda m: m[1]['index'])
    return [m[0] for m in M]


def dialects():
    D = sorted(settings.DIALECTS.items(), key=lambda d: d[1]['index'])
    return [d[0] for d in D]


def dialect_choices():
    return [ (d, Dialect(d).name) for d in dialects() ]


class Method(object):
    def __init__(self, method):
        if method in methods():
            self.method = settings.METHODS[method]
        else:
            raise KeyError

    @property
    def name(self):
        return self.method['name']

    @property
    def title(self):
        return self.method['title']

    @property
    def target(self):
        return self.method['target']

    @property
    def options(self):
        if 'options' in self.method:
            return self.method['options']
        else:
            return []

    @property
    def option_choices(self):
        return ( (self.options.index(option), option['label']) for option in self.options )

    @property
    def cmd(self):
        return self.method['cmd']


class Dialect(object):
    def __init__(self, dialect):
        if dialect in dialects():
            self.dialect = settings.DIALECTS[dialect]
        else:
            raise KeyError

    @property
    def index(self):
        return self.dialect['index']

    @property
    def name(self):
        return self.dialect['name']

    @property
    def cmds(self):
        return self.dialect['cmds']
