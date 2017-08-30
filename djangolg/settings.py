from __future__ import unicode_literals

from django.conf import settings

# Network display name
NETNAME = getattr(settings, 'DJANGOLG_NETNAME', "Example Network")

# General contact email
GENERAL_EMAIL = getattr(settings, 'DJANGOLG_GENERAL_EMAIL', "contact@example.com")
SUPPORT_EMAIL = getattr(settings, 'DJANGOLG_SUPPORT_EMAIL', None)
NOC_EMAIL = getattr(settings, 'DJANGOLG_NOC_EMAIL', None)
PEERING_EMAIL = getattr(settings, 'DJANGOLG_PEERING_EMAIL', None)

# Lifetime of session authorisation key in seconds
# Set to 0 for unlimited
LIFETIME = getattr(settings, 'DJANGOLG_LIFETIME', 300)

# Maximum number of requests with the same key
# Set to 0 for unlimited
MAX_REQUESTS = getattr(settings, 'DJANGOLG_MAX_REQUESTS', 20)

# Default salt value for authorisation key generation
SALT = getattr(settings, 'DJANGOLG_SALT', '_signing_salt_')

# Link to Acceptable Use Policy
AUP_LINK = getattr(settings, 'DJANGOLG_AUP_LINK', None)

# Google reCapture settings
RECAPTCHA_ON = getattr(settings, 'DJANGOLG_RECAPTCHA_ON', False)
RECAPTCHA_URL = getattr(settings, 'DJANGOLG_RECAPTCHA_URL', 'https://www.google.com/recaptcha/api/siteverify')

# Base template
BASE_TEMPLATE = getattr(settings, 'DJANGOLG_BASE_TEMPLATE', 'djangolg/base.html')

# Logo Image
LOGO = getattr(settings, 'DJANGOLG_LOGO', 'djangolg/img/logo.jpg')

# Small Logo Image
SMALL_LOGO = getattr(settings, 'DJANGOLG_SMALL_LOGO', 'djangolg/img/small_logo.jpg')

# Favicon
FAVICON = getattr(settings, 'DJANGOLG_FAVICON', 'djangolg/img/favicon.ico')

# Navbar Image
NAV_IMG = getattr(settings, 'DJANGOLG_NAV_IMG', None)

# Output formatting
FORMATTED_OUTPUT = getattr(settings, 'DJANGOLG_FORMATTED_OUTPUT', False)
