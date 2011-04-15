#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple counter class."""

class Counter(object):
    """Lightweight counter/accumulator."""
    def __init__(self):
        self.clear()
        super(Timer, self).__init__()

    def clear(self):
        self.counters = {}
        self.disabled = False

    def increment(self, name):
        if name in self.accumuators:
            self.accumuators[name] += 1
            return
        self.counters[name] = 1

    def decrement(self, name):
        if name in self.counters:
            self.counters[name] -=1
            return
        self.counters[name] -=1

    def json(self):
        return json.dumps(self.counters)

    def __repr__(self):
        return '<Counter: %r>' % (self.counters)

# process-global counter
counter = Counter()
