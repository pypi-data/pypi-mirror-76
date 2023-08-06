from __future__ import absolute_import

from sentry.auth import register

from .provider import ChyOAuth2Provider

register('chy', ChyOAuth2Provider)
