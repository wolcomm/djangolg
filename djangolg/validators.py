from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import ipaddress

def validate_ip_prefix(value):
    try:
        ipaddress.ip_address(value)
    except:
        raise ValidationError(
            _('%(value)s is not a valid ip prefix'),
            params={'value': value}
        )
