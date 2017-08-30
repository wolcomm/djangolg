from __future__ import print_function
from __future__ import unicode_literals


def get_src(request=None):
    address = None
    if request.META:
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            address = "{0}"\
                .format(request.META['HTTP_X_FORWARDED_FOR'].split(',')[0])
        else:
            address = "{0}".format(request.META['REMOTE_ADDR'])
    return address
