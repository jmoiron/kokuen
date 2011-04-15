#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Kokuen -> Django settings."""

from django.conf import settings

# TODO: i don't like this, should be module paths to prefab filters

defaults = {
    'ENABLE_TIMER' : True,
    'ENABLE_COUNTER' : True,
    'ENABLE_MEMORY' : True,
    'ENABLE_LOAD': True,
}

KOKUEN_SETTINGS = getattr(settings, 'KOKUEN_SETTINGS', defaults)

