from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from djangolg import ip_prefix


class IPPrefixField(forms.CharField):
    def to_python(self, value):
        if not value:
            return None
        try:
            prefix = ip_prefix.IPPrefix(value)
        except:
            raise ValidationError(
                _('%(value)s is not a valid ip prefix'),
                params={'value': value}
            )
        return prefix