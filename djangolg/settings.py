import os

# Network display name
NETNAME = "Example Network"

# General contact email
GENERAL_EMAIL = "contact@example.com"
SUPPORT_EMAIL = None
NOC_EMAIL = None
PEERING_EMAIL = None

# Lifetime of session authorisation key in seconds
# Set to 0 for unlimited
LIFETIME = 300

# Maximum number of requests with the same key
# Set to 0 for unlimited
MAX_REQUESTS = 20

# Default salt value for authorisation key generation
SALT = '_signing_salt_'

# Link to Acceptable Use Policy
AUP_LINK = None

# Google reCapture settings
RECAPTCHA_ON = False
RECAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'

# Base template
BASE_TEMPLATE = 'djangolg/base.html'

# Logo Image
LOGO = 'djangolg/img/logo.jpg'

# Small Logo Image
SMALL_LOGO = 'djangolg/img/small_logo.jpg'

# Favicon
FAVICON = 'djangolg/img/favicon.ico'

# Navbar Image
NAV_IMG = None

# Output formatting
FORMATTED_OUTPUT = False
TEXTFSM_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'textfsm')

#################################################################
# Don't edit below this line!

try:
    from djangolg.local_settings import *
except Exception:
    pass
