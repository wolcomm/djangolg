from djangolg.methods.builtin import (
    BGPPrefixMethod,
    BGPASPathMethod,
    BGPCommunityMethod,
    PingMethod,
    TracerouteMethod
)

def available_methods(output="map"):
    from djangolg.methods.base import BaseMethod
    classes = BaseMethod.__subclasses__()
    if output == "map":
        return {m.name: m for m in classes}
    if output == "list":
        return [m.name for m in classes]
    else:
        raise ValueError("invalid output type: {0}".format(output))

def get_method(name=None):
    return available_methods(output="map")[name]()
