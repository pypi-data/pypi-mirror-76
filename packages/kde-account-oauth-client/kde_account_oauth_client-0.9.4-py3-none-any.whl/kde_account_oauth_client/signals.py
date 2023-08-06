from django.dispatch import Signal

user_created = Signal(providing_args=['instance', 'oauth_info'])
"""Sent when a user is created by logging in via KDE Account.

:param instance: the user model instance.
:param oauth_info: the info dict received from KDE Account, contains
    'id', 'nickname', 'email', 'full_name', and possibly other keys.
"""
