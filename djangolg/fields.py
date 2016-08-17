import ipaddress
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from djangolg import types


# TODO: Provide options to disallow reserved/multicast addresses
class IPPrefixField(forms.CharField):
    def to_python(self, value):
        if not value:
            return None
        try:
            prefix = types.IPPrefix(value)
        except:
            raise ValidationError(
                _('%(value)s is not a valid ip prefix'),
                params={'value': value}
            )
        return prefix


class IPAddressField(forms.CharField):
    def to_python(self, value):
        if not value:
            return None
        try:
            address = ipaddress.ip_address(value)
        except:
            raise ValidationError(
                _('%(value)s is not a valid ip address'),
                params={'value': value}
            )
        return address


class RouterChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        try:
            label = obj.label
        except NotImplementedError:
            label = str(obj)
        return label
