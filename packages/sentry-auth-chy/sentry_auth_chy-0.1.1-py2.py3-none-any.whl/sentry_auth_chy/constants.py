from __future__ import absolute_import, print_function

from django.conf import settings


AUTHORIZE_URL = getattr(settings, 'AUTHORIZE_URL', None)

ACCESS_TOKEN_URL = getattr(settings, 'ACCESS_TOKEN_URL', None)

CLIENT_ID = getattr(settings, 'CHY_CLIENT_ID', None)

CLIENT_SECRET = getattr(settings, 'CHY_CLIENT_SECRET', None)

ERR_INVALID_DOMAIN = 'The domain for your Chy account (%s) is not allowed to authenticate with this provider.'

ERR_INVALID_RESPONSE = 'Unable to fetch user information from Chy.  Please check the log.'

SCOPE = 'email'

DOMAIN_BLOCKLIST = frozenset(getattr(settings, 'CHY_DOMAIN_BLOCKLIST', ['gmail.com']) or [])

DATA_VERSION = '1'
