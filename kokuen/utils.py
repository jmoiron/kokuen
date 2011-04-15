#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities for kokuen."""

def to_bytes(string):
    """Converts a string with a human-readable byte size to a number of
    bytes.  Takes strings like '7536 kB', in the format of proc."""
    num, units = string.split()
    num = int(num)
    powers = {'kb': 10, 'mb': 20, 'gb': 30}
    if units and units.lower() in powers:
        num <<= powers[units.lower()]
    return num

def bytes_to_string(bytes):
    """Converts number of bytes to a string.  Based on old code here:
    Uses proc-like units (capital B, lowercase prefix).  This only takes a
    few microseconds even for numbers in the terabytes.
    """
    units = ['B', 'kB', 'mB', 'gB', 'tB']
    negate = bytes < 0
    if negate: bytes = -bytes
    factor = 0
    while bytes/(1024.0**(factor+1)) >= 1:
        factor += 1
    return '%s%0.1f %s' % ('-' if negate else '', bytes/(1024.0**factor), units[factor])


