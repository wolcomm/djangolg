from djangolg import settings


def methods():
    return settings.METHODS.keys()


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
    def form(self):
        return self.method['form']

    @property
    def title(self):
        return self.method['title']

    @property
    def target(self):
        return self.method['target']

    @property
    def options(self):
        return self.method['options']

    @property
    def cmd(self):
        return self.method['cmd']
