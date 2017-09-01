# Copyright 2017 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Configuration settings for djangolg."""

from __future__ import unicode_literals

from django.conf import settings

# Network display name
NETNAME = getattr(settings, 'DJANGOLG_NETNAME', "Example Network")

# General contact email
GENERAL_EMAIL = getattr(settings, 'DJANGOLG_GENERAL_EMAIL',
                        "contact@example.com")
SUPPORT_EMAIL = getattr(settings, 'DJANGOLG_SUPPORT_EMAIL', None)
NOC_EMAIL = getattr(settings, 'DJANGOLG_NOC_EMAIL', None)
PEERING_EMAIL = getattr(settings, 'DJANGOLG_PEERING_EMAIL', None)

# Router name display function
ROUTER_LABEL = getattr(
    settings, 'DJANGOLG_ROUTER_LABEL',
    lambda router:
        router.location.name if router.location else str(router)
)

# Lifetime of session authorisation key in seconds
# Set to 0 for unlimited
LIFETIME = getattr(settings, 'DJANGOLG_LIFETIME', 300)

# Maximum number of requests with the same key
# Set to 0 for unlimited
MAX_REQUESTS = getattr(settings, 'DJANGOLG_MAX_REQUESTS', 20)

# Link to Acceptable Use Policy
AUP_LINK = getattr(settings, 'DJANGOLG_AUP_LINK', None)

# Google reCapture settings
RECAPTCHA_ON = getattr(settings, 'DJANGOLG_RECAPTCHA_ON', False)
RECAPTCHA_URL = getattr(settings, 'DJANGOLG_RECAPTCHA_URL',
                        'https://www.google.com/recaptcha/api/siteverify')
RECAPTCHA_SITE_KEY = getattr(settings, 'DJANGOLG_RECAPTCHA_SITE_KEY', None)
RECAPTCHA_SECRET_KEY = getattr(settings, 'DJANGOLG_RECAPTCHA_SECRET_KEY', None)

# Base template
BASE_TEMPLATE = getattr(settings, 'DJANGOLG_BASE_TEMPLATE',
                        'djangolg/base.html')

# Logo Image
LOGO = getattr(settings, 'DJANGOLG_LOGO', 'djangolg/img/logo.jpg')

# Small Logo Image
SMALL_LOGO = getattr(settings, 'DJANGOLG_SMALL_LOGO',
                     'djangolg/img/small_logo.jpg')

# Favicon
FAVICON = getattr(settings, 'DJANGOLG_FAVICON', 'djangolg/img/favicon.ico')

# Navbar Image
NAV_IMG = getattr(settings, 'DJANGOLG_NAV_IMG', None)

# Output formatting
FORMATTED_OUTPUT = getattr(settings, 'DJANGOLG_FORMATTED_OUTPUT', False)

# Enable debugging
# this will re-raise exceptions in the view, so that stack traces
# can be inspected
DEBUG = getattr(settings, 'DJANGOLG_DEBUG', False)
