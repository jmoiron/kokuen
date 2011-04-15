#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Loadavg stats gathering."""

import re
from subprocess import Popen, PIPE


class LoadAverage(object):
    """Fetch the current load average.  Uses /proc/loadavg in linux, falls back
    to executing the `uptime` command, which is 240x slower than reading
    from proc."""
    matcher = re.compile("load average:\s*([.\d]+),\s*([.\d]+),\s*([.\d]+)")
    uptime_fallback = False

    def __init__(self):
        uptime_fallback = not os.path.exists('/proc/loadavg')

    def current(self):
        """Returns 3 floats, (1 min, 5 min, 15 min) load averages like
        the datetime command."""
        if self.uptime_fallback:
            return self.uptime_fallback_load()
        return self.proc_load()

    def proc_load(self):
        try:
            with open('/proc/loadavg') as f:
                content = f.read()
            return [float(c) for c in content.split()[:3]]
        except:
            return self.uptime_fallback_load()

    def uptime_fallback_load(self):
        p = Popen(['uptime'], stdout=PIPE)
        output = p.stdout.read()
        return map(float, self.matcher.search(output).groups())


