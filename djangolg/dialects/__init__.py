from __future__ import print_function
from __future__ import unicode_literals

from djangolg.dialects.builtin import ( #noqa
    CiscoIOSDialect
)


def available_dialects(output="map"):
    from djangolg.dialects.base import BaseDialect
    classes = BaseDialect.__subclasses__()
    if output == "map":
        return {d.name: d for d in classes}
    if output == "choices":
        return [(d.name, d.description) for d in classes]
    if output == "list":
        return [d.name for d in classes]
    else:
        raise ValueError("invalid output type: {0}".format(output))


def get_dialect(name=None):
    return available_dialects(output="map")[name]()
