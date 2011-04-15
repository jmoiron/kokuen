#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Timing helpers."""

import time

try:
    import simplejson as json
except ImportError:
    import json

class Timer(threading.local):
    """Lightweight timing class.  Stores both absolute time of given events and
    accumulated times of one or more arbitrary start/stop pairs."""
    def __init__(self):
        self.clear()
        super(Timer, self).__init__()

    def clear(self):
        self.checkpoints = []
        self.accumulators = {}
        self.disabled = False

    def disable(self):
        self.disabled = True

    def checkpoint(self, name):
        if self.disabled: return
        t = time.time()
        self.checkpoints.append((name, t))

    def start(self, name):
        if self.disabled: return
        t0 = time.time()
        if name in self.accumulators and self.accumulators[name].get('t0', None):
            # XXX: we tried to start an accumulator twice without ending it..
            # that's bad, we shouldn't allow that
            return
        self.accumulators.setdefault(name, {'dt': 0})['t0'] = t0

    def stop(self, name):
        if self.disabled: return
        t1 = time.time()
        if name not in self.accumulators or not self.accumulators[name].get('t0', 0):
            # XXX: we are trying to stop an accumulator that doesn't exist or
            # wasn't started, which we also should do something about
            return
        acc = self.accumulators[name]
        if 'called' not in acc:
            acc['called'] = 0
        acc['called'] += 1
        dt = t1 - acc['t0']
        del acc['t0']
        acc['dt'] += dt

    def json(self):
        acc = self.accumuators
        return json.dumps({
            'checkpoints' : self.checkpoints,
            'accumulators' : dict([(key, (acc[key]['called'], acc[key]['dt'])) for key in acc]),
        })

    def as_header(self):
        return base64.b64encode(self.json())

    def __repr__(self):
        return repr({'checkpoints' : self.checkpoints, 'accumulators' : self.accumulators})

# process-global timer
timer = Timer()

