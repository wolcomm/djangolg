from django.core.signing import TimestampSigner
from djangolg import settings

signer = TimestampSigner()
if settings.SALT: signer.salt = settings.SALT


class AuthKey(object):
    def __init__(self, value=None):
        self.data = {
            'clear': value,
            'signed': signer.sign(value)
        }

    @property
    def clear(self):
        return self.data['clear']

    @property
    def signed(self):
        return self.data['signed']

    def validate(self, key):
        try:
            clear = signer.unsign(key, max_age=settings.LIFETIME)
            if self.clear == clear:
                return True
            else:
                raise ValueError
        except Exception:
            raise

    def __str__(self):
        return self.signed

    def __unicode__(self):
        return self.__str__()
